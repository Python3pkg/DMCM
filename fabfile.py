"""
Fabfile for ahernp.com.
"""
from fabric.api import * 
from fabric.contrib.console import confirm

env.hosts = ['web']

def test():
    with settings(warn_only=True):
        result = local('python manage.py test', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

                  
def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '~/project'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
          run("git clone git@github.com:ahernp/DMCM.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("~/webapps/django/apache2/bin/restart")

