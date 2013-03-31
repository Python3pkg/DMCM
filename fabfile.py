"""Fabfile for DMCM."""
import codecs
import os
from fabric.api import (env, local, lcd, cd, run,
                        task, hosts, settings, abort,
                        prefix)
from fabric.colors import magenta, yellow
from fabric.contrib.console import confirm
from fabric.operations import get
from datetime import datetime
from decorator import decorator

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
PARENT_PATH = os.path.join(PROJECT_PATH, os.pardir)

VIRTUALENV_PACKAGES = os.path.join(PARENT_PATH, 'lib', 'python2.7', 'site-packages')

# PIP requirements file
REQUIREMENTS = """Django==1.5.1
Markdown==2.2.1
MySQL-python==1.2.4
argparse==1.2.1
django-reversion==1.7
feedparser==5.1.3
wsgiref==0.1.2
-e git://github.com/ahernp/django-monitoring.git#egg=django-bugtracker
-e git://github.com/ahernp/django-monitoring.git#egg=django-monitoring
django-feedreader==0.5.0
"""

LOCALSETTINGS = """DEBUG = True
DEVELOP = True
SECRET_KEY = 'Default for testing; Override with random data when deployed'
"""

AUTH_JSON = """[
    {
        "pk": 1,
        "model": "auth.user",
        "fields": {
            "username": "ahernp",
            "first_name": "",
            "last_name": "",
            "is_active": true,
            "is_superuser": true,
            "is_staff": true,
            "last_login": "2012-05-11 20:20:51",
            "groups": [],
            "user_permissions": [],
            "password": "",
            "email": "",
            "date_joined": "2010-05-22 15:14:56"
        }
    }
]
"""

STATIC_FILES = [{
                'path': os.path.join(PARENT_PATH, 'requirements.txt'),
                'data': REQUIREMENTS,
                },
                {
                'path': os.path.join(PROJECT_PATH, 'localsettings.py'),
                'data': LOCALSETTINGS,
                },
                {
                'path': os.path.join(PROJECT_PATH, 'dmcm', 'fixtures', 'auth.json'),
                'data': AUTH_JSON,
                }]

env.hosts = ['web']


def write_file(filename, data):
    """Write data to file."""
    output_file = codecs.open(filename, 'w', 'utf-8')
    output_file.write(data)
    output_file.close()


@decorator
def timer(func, *args, **kwargs):
    """Wrapper which outputs how long a function took to run."""
    start_time = datetime.now()
    result = func(*args, **kwargs)
    end_time = datetime.now()
    duration = end_time - start_time
    print(magenta('# {} ran for {} (started at {:%H:%M:%S}, ended at {:%H:%M:%S})'
          .format(func.__name__, duration, start_time, end_time)))
    return result


@task
@timer
def setup():
    """Setup development environment in current virtualenv."""
    for output_file in STATIC_FILES:
        if not os.path.isfile(output_file['path']):
            print(yellow('# Writing file \'%s\'' % (output_file['path'])))
            write_file(output_file['path'], output_file['data'])

    with lcd(PARENT_PATH):
        local('pip install -r requirements.txt')

    # Get current data from live
    if confirm('Get data from live system?'):
        CODE_DIR = '~/project'
        with cd(CODE_DIR):
            with prefix('export PYTHONPATH="/home/ahernp/webapps/django:$PYTHONPATH"'):
                run('python2.7 manage.py dumpdata --indent 4 dmcm sites.site feedreader.options feedreader.group feedreader.feed > ~/initial_data.json')
        get('initial_data.json', os.path.join(PROJECT_PATH, 'initial_data.json'))

    # Recreate database
    with settings(warn_only=True), lcd(PROJECT_PATH):
        local('rm dmcm.sqlite3')
    manage('syncdb --noinput')
    manage('loaddata auth.json')
    manage('collectstatic --noinput')
    with settings(warn_only=True), lcd(PROJECT_PATH):
        local('echo "UPDATE feedreader_feed SET published_time = NULL;" | sqlite3 dmcm.sqlite3')


@task
@hosts('localhost')
@timer
def test():
    """Run Django Unit Tests."""
    with settings(warn_only=True), lcd(PROJECT_PATH):
        result = local('python manage.py test', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


@task
@timer
def deliver():
    """Test, commit and push changes. """
    local("git status")
    with lcd(PROJECT_PATH):
        local('grep -r --include="*.py" "pdb" . || [ $? -lt 2 ]')
        # grep issues a return code of 1 if no matches were found
        # '|| [ $? -lt 2 ]' ensures a zero return code to local
    if not confirm('Check status. Continue with delivery?'):
        abort('Aborting at user request.')
    test()
    local("git add -p && git commit")
    local("git push")


@task
@timer
def deploy():
    """Deploy dmcm onto live server."""
    code_dir = '~/project'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:ahernp/DMCM.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("~/webapps/django/apache2/bin/restart")


@task
@hosts('localhost')
@timer
def manage(*args, **kwargs):
    """Locally execute Django command."""
    with settings(warn_only=True):
        with lcd(PROJECT_PATH):
            local('python manage.py %s %s' % (' '.join(args),
                                              ' '.join(['%s=%s' % (option, kwargs[option]) for option in kwargs])))
