"""
Fabfile for ahernp.com.
"""
import os
from fabric.api import (env, local, lcd, cd, run, 
                        task, hosts, settings, abort,
                        prefix)
from fabric.contrib.console import confirm
from fabric.operations import get
from datetime import datetime
from decorator import decorator

TOP_LEVEL_PATH = os.path.dirname(os.path.realpath(__file__))

env.hosts = ['web']

@decorator
def timer(func, *args, **kwargs):
    """Wrapper which outputs how long a function took to run."""
    start_time = datetime.now()
    result = func(*args, **kwargs)
    end_time = datetime.now()
    duration = end_time - start_time
    print('# {} ran for {} (started at {:%H:%M:%S}, ended at {:%H:%M:%S})'\
          .format(func.__name__, duration, start_time, end_time))
    return result

@task
def setup():
    """Setup development environment."""
    #with lcd(TOP_LEVEL_PATH):
    #    local('git pull')
    code_dir = '~/project'
    with cd(code_dir):
        with prefix('export PYTHONPATH="/home/ahernp/webapps/django:$PYTHONPATH"'):
            run('python2.7 manage.py dumpdata --indent 4 dmcm > ~/initial_data.json')
    get('initial_data.json', os.path.join(TOP_LEVEL_PATH, 'dmcm', 'fixtures', 'initial_data.json'))
    with lcd(TOP_LEVEL_PATH):
        local('python manage.py syncdb')
        local('python manage.py runserver')

@task
@timer
@hosts('localhost')
def test():
    """Test dmcm."""
    with settings(warn_only=True), lcd(TOP_LEVEL_PATH):
        result = local('python manage.py test dmcm', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

@task
@timer
def deliver():
    """Add and commit changes"""
    local("git add -p && git commit")

@task
@timer        
def prepare_deploy():
    """Test, commit and push changes. """
    test()
    deliver()
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
@timer
@hosts('localhost')
def manage(*args):
    """Locally execute Django command."""
    with settings(warn_only=True):
        with lcd(TOP_LEVEL_PATH):
            local('python manage.py %s' % (' '.join(args)))
