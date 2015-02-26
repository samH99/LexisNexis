from .timeparse import parse_timedelta

import logging
log = logging.getLogger(__name__)

class TimeInfo(object):
    """
    This is a simple object that calculates and stores datetime information for an XModule
    based on the due date and the grace period string

    So far it parses out three different pieces of time information:
        self.display_due_date - the 'official' due date that gets displayed to students
        self.grace_period - the length of the grace period
        self.close_date - the real due date

    """
    def __init__(self, due_date, grace_period_string):
        if due_date is not None:
            self.display_due_date = due_date

        else:
            self.display_due_date = None

        if grace_period_string is not None and self.display_due_date:
            try:
                self.grace_period = parse_timedelta(grace_period_string)
                self.close_date = self.display_due_date + self.grace_period
            except:
                log.error("Error parsing the grace period {0}".format(grace_period_string))
                raise
        else:
            self.grace_period = None
            self.close_date = self.display_due_date
