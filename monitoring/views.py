from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from monitoring.models import Log


@login_required
def dashboard(request):
    """
    Build page providing information about the state of the system.
    """
    import django
    import reversion
    import markdown
    import os
    from subprocess import Popen, PIPE

    # Shell commands: Name and command
    SHELL_COMMANDS = [
        ('hostname', 'hostname'),
        ('gitversion', 'git log -n 1'),
        ('mysql_version', 'mysql --version'),
    ]

    # Flags in settings: Their expected  and actual values.
    SETTINGS_FLAGS = [
        ('DEBUG', False),
        ('DEVELOP', False),
    ]

    def run_shell_command(command, cwd):
        """
        Run command in shell and return results.
        """
        p = Popen(command, shell=True, cwd=cwd, stdout=PIPE)
        stdout = p.communicate()[0]
        if stdout:
            stdout = stdout.strip()
        return stdout

    context = {}

    # Versions
    context['django_version'] = '.'.join(str(i) for i in django.VERSION)
    context['markdown_version'] = '.'.join(str(i) for i in markdown.version_info)
    context['reversion_version'] = '.'.join(str(i) for i in reversion.VERSION)

    curr_dir = os.path.realpath(os.path.dirname(__file__))
    for name, shell_command in SHELL_COMMANDS:
        context[name] = run_shell_command(shell_command, curr_dir)

    # Settings Flags
    context['settings_flags'] = []
    for name, expected in SETTINGS_FLAGS:
        actual_setting = getattr(settings, name, None)
        context['settings_flags'].append({
            'name': name,
            'unexpected': expected != actual_setting,
            'actual': actual_setting
        })

    context['error_msgs'] = Log.objects.filter(level='ERROR')[:2]
    context['warning_msgs'] = Log.objects.filter(level='WARNING')[:2]
    context['info_msgs'] = Log.objects.filter(level='INFO')[:2]

    context['time_checked'] = datetime.now()
    return render_to_response('monitoring/dashboard.html', context, RequestContext(request))
