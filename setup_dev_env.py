#!/usr/bin/env python
"""
Python Script to setup development environment.
"""
import codecs, os, sys
from subprocess import Popen, PIPE, STDOUT

TOP_LEVEL_DIRECTORY = os.path.expanduser('~/code/dmcm')
PROJECT_DIRECTORY = os.path.join(TOP_LEVEL_DIRECTORY, 'project')

APPLICATIONS = [
                {
                'name': 'dmcm',
                'directory': os.path.join(TOP_LEVEL_DIRECTORY, 'project'),
                'path_to': TOP_LEVEL_DIRECTORY,
                'update': 'git pull',
                'clone': 'git clone git@github.com:ahernp/DMCM.git project',
                },
                {
                'name': 'django',
                'directory': os.path.join(TOP_LEVEL_DIRECTORY, 'django'),
                'path_to': TOP_LEVEL_DIRECTORY,
                'update': 'svn up',
                'clone': 'svn co http://code.djangoproject.com/svn/django/branches/releases/1.4.X/django',
                },
                {
                'name': 'markdown',
                'directory': os.path.join(TOP_LEVEL_DIRECTORY, 'markdown'),
                'path_to': TOP_LEVEL_DIRECTORY,
                'update': 'git pull',
                'clone': 'git clone git://github.com/waylan/Python-Markdown.git markdown',
                },
                {
                'name': 'reversion',
                'directory': os.path.join(TOP_LEVEL_DIRECTORY, 'reversion', 'src', 'reversion'),
                'path_to': os.path.join(TOP_LEVEL_DIRECTORY, 'reversion', 'src'),
                'update': 'git pull',
                'clone': 'git clone https://github.com/etianen/django-reversion.git reversion',
                },
]

VIRTUALENV_PYTHON = os.path.join(TOP_LEVEL_DIRECTORY, 'bin', 'python')
VIRTUALENV_PACKAGES = os.path.join(TOP_LEVEL_DIRECTORY, 'lib', 'python2.7', 'site-packages')
EXTRA_PATHS_FILE = os.path.join(VIRTUALENV_PACKAGES, 'extra.pth')

DATABASE_NAME = 'dmcm'
DROP_DATABASE = 'mysql --user=root --execute="drop database if exists %s"' % (DATABASE_NAME)
CREATE_DATABASE = 'mysql --user=root --execute="create database if not exists %s character set utf8"' % (DATABASE_NAME)

COMMANDS = [{'django': False, 'command': 'mysql --user=root --execute="drop database if exists %s"' % (DATABASE_NAME)},
            {'django': False, 'command': 'mysql --user=root --execute="create database if not exists %s character set utf8"' % (DATABASE_NAME)},
            {'django': True, 'command': 'syncdb --noinput'},
            {'django': True, 'command': 'loaddata auth.json'},
            {'django': True, 'command': 'collectstatic --noinput'},
]

LOCALSETTINGS = """DEBUG = True
DEVELOP = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmcm',
        'USER': '',
        'PASSWORD': '',
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

output_files = [
                {
                'name': os.path.join(PROJECT_DIRECTORY, 'localsettings.py'),
                'data': LOCALSETTINGS,
                },
                {
                'name': os.path.join(PROJECT_DIRECTORY, 'dmcm', 'fixtures', 'auth.json'),
                'data': AUTH_JSON,
                },
]

def run_shell_command(command, cwd):
    """
    Run command in shell and return results.
    """
    p = Popen(command, shell=True, cwd=cwd, stdout=PIPE)
    stdout = p.communicate()[0]
    if stdout:
        stdout = stdout.strip()
    print('# Command \'%s\' returned: %s' % (command, '...%s' % (stdout[-200:]) if len(stdout) > 200 else stdout))
    return stdout

def run_django_command(command):
    run_shell_command('%s manage.py %s' % (VIRTUALENV_PYTHON, command), PROJECT_DIRECTORY)

def write_file(filename, data):
    output_file = codecs.open(filename, 'w', 'utf-8')
    output_file.write(data)
    output_file.close()

#import pdb; pdb.set_trace() # Start debugging

if not os.path.isdir(TOP_LEVEL_DIRECTORY):
    print('# Create directory or virtualenvironment at "%s"' % (TOP_LEVEL_DIRECTORY))
    sys.exit()

application_directories = set()
print('# Clone or update application repositories:')
for application in APPLICATIONS:
    if os.path.isdir(application['directory']):
        print('# Updating %s' % (application['name']))
        run_shell_command(application['update'], application['directory'])
    else:
        print('# Cloning %s' % (application['name']))
        run_shell_command(application['clone'], TOP_LEVEL_DIRECTORY)
    application_directories.add(application['path_to'])

if os.path.isdir(VIRTUALENV_PACKAGES):
    print('# Add paths to applications to PYTHONPATH. (%s)' % (', '.join(application_directories)))
    output_files.append({'name': EXTRA_PATHS_FILE, 'data': '\n'.join(application_directories)})

for output_file in output_files:
    if not os.path.isfile(output_file['name']):
        print('# Writing file \'%s\'' % (output_file['name']))
        write_file(output_file['name'], output_file['data'])

print('# Recreate database "%s"' % (DATABASE_NAME))
for command in COMMANDS:
    if command['django']:
        run_django_command(command['command'])
    else:
        run_shell_command(command['command'], TOP_LEVEL_DIRECTORY)
