import time, glob
from django.core.management.base import BaseCommand, CommandError
from annoying.functions import get_object_or_None
from main.models import VideoFile
from utils.videos import download_video
from utils.jobs import force_job
from utils.general import break_into_chunks

import settings

class Command(BaseCommand):
    help = "Sync up the database's version of what videos have been downloaded with the actual folder contents"

    def handle(self, *args, **options):

        # delete VideoFile objects that are not marked as in progress, but are neither 0% nor 100% done; they're broken
        VideoFile.objects.filter(download_in_progress=False, percent_complete__gt=0, percent_complete__lt=100).delete()

        files = glob.glob(settings.CONTENT_ROOT + "*.mp4")
        subtitle_files = glob.glob(settings.CONTENT_ROOT + "*.srt")
        videos_marked_at_all = set([video.youtube_id for video in VideoFile.objects.all()])
        videos_marked_as_in_progress = set([video.youtube_id for video in VideoFile.objects.filter(download_in_progress=True)])
        videos_marked_as_unstarted = set([video.youtube_id for video in VideoFile.objects.filter(percent_complete=0, download_in_progress=False)])
        
        videos_in_filesystem = set([path.replace("\\", "/").split("/")[-1].split(".")[0] for path in files])
        videos_in_filesystem_chunked = break_into_chunks(videos_in_filesystem)

        videos_flagged_for_download = set([video.youtube_id for video in VideoFile.objects.filter(flagged_for_download=True)])

        subtitles_in_filesystem = set([path.replace("\\", "/").split("/")[-1].split(".")[0] for path in subtitle_files])
        subtitles_in_filesystem_chunked = break_into_chunks(subtitles_in_filesystem)
        
        count = 0
        for chunk in videos_in_filesystem_chunked:
            video_files_needing_model_update = VideoFile.objects.filter(percent_complete=0, download_in_progress=False, youtube_id__in=chunk)
            count += video_files_needing_model_update.count()
            video_files_needing_model_update.update(percent_complete=100, flagged_for_download=False)
        if count:
            self.stdout.write("Updated %d VideoFile models (to mark them as complete, since the files exist)\n" % count)
        
        video_ids_needing_model_creation = list(videos_in_filesystem - videos_marked_at_all)
        count = len(video_ids_needing_model_creation)
        if count:
            VideoFile.objects.bulk_create([VideoFile(youtube_id=youtube_id, percent_complete=100) for youtube_id in video_ids_needing_model_creation])
            self.stdout.write("Created %d VideoFile models (to mark them as complete, since the files exist)\n" % count)
        
        count = 0
        videos_needing_model_deletion_chunked = break_into_chunks(videos_marked_at_all - videos_in_filesystem - videos_flagged_for_download)
        for chunk in videos_needing_model_deletion_chunked:
            video_files_needing_model_deletion = VideoFile.objects.filter(youtube_id__in=chunk)
            count += video_files_needing_model_deletion.count()
            video_files_needing_model_deletion.delete()
        if count:
            self.stdout.write("Deleted %d VideoFile models (because the videos didn't exist in the filesystem)\n" % count)

        count = 0
        for chunk in subtitles_in_filesystem_chunked:
            video_files_needing_model_update = VideoFile.objects.filter(subtitle_download_in_progress=False, subtitles_downloaded=False, youtube_id__in=chunk)
            count += video_files_needing_model_update.count()
            video_files_needing_model_update.update(subtitles_downloaded=True)
        if count:
            self.stdout.write("Updated %d VideoFile models (marked them as having subtitles)\n" % count)
        