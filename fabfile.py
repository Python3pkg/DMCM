"""
Fabfile for ahernp.com.
"""
import codecs, os
from fabric.api import (env, local, lcd, cd, run,
                        task, hosts, settings, abort,
                        prefix)
from fabric.colors import magenta, yellow
from fabric.contrib.console import confirm
from fabric.operations import get
from datetime import datetime
from decorator import decorator

DATABASE_NAME = 'dmcm'

DJANGO_PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
PARENT_PATH = os.path.join(DJANGO_PROJECT_PATH, os.pardir)

VIRTUALENV_PACKAGES = os.path.join(PARENT_PATH, 'lib', 'python2.7', 'site-packages')
EXTRA_PYTHONPATHS_FILE = os.path.join(VIRTUALENV_PACKAGES, 'extra.pth')

DEPENDENCIES = [
                {
                'name': 'dmcm',
                'install_dir': 'project',
                'pythonpath': PARENT_PATH,
                'update': 'git pull',
                'clone': 'git clone git@github.com:ahernp/DMCM.git project',
                },
                {
                'name': 'django',
                'install_dir': 'django',
                'pythonpath': PARENT_PATH,
                'update': 'svn up',
                'clone': 'svn co http://code.djangoproject.com/svn/django/branches/releases/1.4.X/django',
                },
                {
                'name': 'markdown',
                'install_dir': 'markdown',
                'pythonpath': os.path.join(PARENT_PATH, 'markdown'),
                'update': 'git pull',
                'clone': 'git clone git://github.com/waylan/Python-Markdown.git markdown',
                },
                {
                'name': 'reversion',
                'install_dir': 'reversion',
                'pythonpath': os.path.join(PARENT_PATH, 'reversion', 'src'),
                'update': 'git pull',
                'clone': 'git clone https://github.com/etianen/django-reversion.git reversion',
                },
]

LOCALSETTINGS = """DEBUG = True
DEVELOP = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmcm',
        'USER': 'root',
    }
}
SECRET_KEY = ''
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

STATIC_FILES = [
                {
                'path': os.path.join(DJANGO_PROJECT_PATH, 'localsettings.py'),
                'data': LOCALSETTINGS,
                },
                {
                'path': os.path.join(DJANGO_PROJECT_PATH, 'dmcm', 'fixtures', 'auth.json'),
                'data': AUTH_JSON,
                },
]

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
    print(magenta('# {} ran for {} (started at {:%H:%M:%S}, ended at {:%H:%M:%S})'\
          .format(func.__name__, duration, start_time, end_time)))
    return result

@task
@timer
def setup():
    """Setup development environment."""
    repo_dirs = set() # Directories needed on pythonpath
    for repo in DEPENDENCIES:
        install_path = os.path.join(PARENT_PATH, repo['install_dir'])
        if os.path.exists(install_path):
            print('# Updating %s' % (repo['name']))
            with lcd(install_path):
                local(repo['update'])
        else:
            print(yellow('# Cloning %s' % (repo['name'])))
            with lcd(PARENT_PATH):
                local(repo['clone'])
        repo_dirs.add(os.path.join(PARENT_PATH, repo['pythonpath']))

    # Ensure dependencies are available on pythonpath.
    print('# Add applications to PYTHONPATH. (%s)' % (', '.join(repo_dirs)))
    static_files = STATIC_FILES
    static_files.append({'path': EXTRA_PYTHONPATHS_FILE,
                         'data': '\n'.join(repo_dirs)})
    if os.path.isfile(EXTRA_PYTHONPATHS_FILE):
        local('rm %s' % (EXTRA_PYTHONPATHS_FILE))
    for output_file in static_files:
        if not os.path.isfile(output_file['path']):
            print('# Writing file \'%s\'' % (output_file['path']))
            write_file(output_file['path'], output_file['data'])

    # Get current data from live
    code_dir = '~/project'
    with cd(code_dir):
        with prefix('export PYTHONPATH="/home/ahernp/webapps/django:$PYTHONPATH"'):
            run('python2.7 manage.py dumpdata --indent 4 dmcm > ~/initial_data.json')
    get('initial_data.json', os.path.join(DJANGO_PROJECT_PATH, 'dmcm', 'fixtures', 'initial_data.json'))

    # Recreate database
    with lcd(DJANGO_PROJECT_PATH):
        local('mysql --user=root --execute="drop database if exists %s"' % (DATABASE_NAME))
        local('mysql --user=root --execute="create database if not exists %s character set utf8"' % (DATABASE_NAME))
    manage('syncdb --noinput')
    manage('loaddata auth.json')
    manage('collectstatic --noinput')

@task
@hosts('localhost')
@timer
def test():
    """Test dmcm."""
    with settings(warn_only=True), lcd(DJANGO_PROJECT_PATH):
        result = local('python manage.py test dmcm', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

@task
@timer
def deliver():
    """Test, commit and push changes. """
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
def manage(*args):
    """Locally execute Django command."""
    with settings(warn_only=True):
        with lcd(DJANGO_PROJECT_PATH):
            local('python manage.py %s' % (' '.join(args)))
