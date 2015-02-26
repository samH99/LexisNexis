"""
Deploy this project in dev/stage/production.

Requires commander_ which is installed on the systems that need it.

.. _commander: https://github.com/oremj/commander
"""
import os
import sys

from commander.deploy import task, hostgroups


# Import commander local settings.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import commander_settings as settings


@task
def update_code(ctx, tag):
    """Update the code to a specific git reference (tag/sha/etc)."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('git fetch')
        ctx.local('git checkout -f %s' % tag)
        ctx.local('git submodule sync')
        ctx.local('git submodule update --init --recursive')


@task
def update_info(ctx):
    """Write info about the current state to a publicly visible file."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('date')
        ctx.local('git branch')
        ctx.local('git log -3')
        ctx.local('git status')
        ctx.local('git submodule status')

        ctx.local('git rev-parse HEAD > static/revision')


@task
def clean(ctx):
    """Clean .gitignore and .pyc files."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("find . -type f -name '.gitignore' -or -name '*.pyc' -delete")


@task
def update_assets(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('python2.6 manage.py collectstatic --noinput --clear')
        # LANG=en_US.UTF-8 is sometimes necessary for the YUICompressor.
        ctx.local('LANG=en_US.UTF8 python2.6 manage.py compress_assets')


@task
def update_db(ctx):
    """
    Update the database schema, if necessary.

    Uses schematic by default. Change to south if you need to.
    """
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('python2.6 manage.py syncdb --noinput')
        ctx.local('python2.6 manage.py migrate --noinput')
        ctx.local('python2.6 manage.py migrate --list')


@task
def update_product_details(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('python2.6 manage.py update_product_details')


@task
def checkin_changes(ctx):
    """Use the local, IT-written deploy script to check in changes."""
    ctx.local(settings.DEPLOY_SCRIPT)


@hostgroups(settings.WEB_HOSTGROUP, remote_kwargs={'ssh_key': settings.SSH_KEY})
def deploy_app(ctx):
    """Call the remote update script to push changes to webheads."""
    ctx.remote('touch %s' % settings.REMOTE_WSGI)


@task
def pre_update(ctx, ref=settings.UPDATE_REF):
    """Update code to pick up changes to this file."""
    update_code(ref)
    update_info()
    clean()


@task
def update(ctx):
    update_assets()
    update_db()
    update_product_details()


@task
def deploy(ctx):
    checkin_changes()
    deploy_app()


@task
def update_site(ctx, tag):
    """Update the app to prep for deployment."""
    pre_update(tag)
    update()


def main():
    """Execute main deploy steps. Useful for non-chief push systems."""
    pre_update()
    update()
    deploy()


if __name__ == "__main__":
    main()
