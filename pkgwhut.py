import sys,os
import platform
import shlex
import subprocess
#import yaml
# debian, CentOS, CentOS Linux, Red Hat Enterprise Linux
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
from get_platform_id import get_platform_id

commands = {
    'which-package-has-file': {
        'Debian': 'dpkg --search {0}',
        'CentOS': 'repoquery --installed -f {0}',
        'Red Hat Enterprise Linux': 'dnf repoquery --installed --file {0}',
        'Ubuntu': 'dpkg --search {0}',
        'Pop!_OS': 'dpkg --search {0}',
        'Arch Linux': 'pkgfile -s {0}',  # Requires pkgfile package
        'Gentoo': 'equery files -f {0}',  # Part of gentoolkit
        'Alpine Linux': 'apk info -W {0}',
        'openSUSE': 'zypper se -f {0}',
        'Fedora': 'dnf repoquery --installed --file {0}',
        'Void Linux': 'xbps-query -o {0}',
        'Manjaro': 'pkgfile -s {0}',  # Requires pkgfile package
        'cygwin': 'cygcheck -f {0}'
    },
    'installed-packages': {
        'Debian': 'dpkg -l',
        'CentOS': 'yum list installed',
        'Red Hat Enterprise Linux': 'dnf list installed',
        'Ubuntu': 'dpkg -l',
        'Pop!_OS': 'dpkg -l',
        'Arch Linux': 'pacman -Q',
        'Gentoo': 'emerge --list-installed',  # Or 'ls /var/db/pkg/*/*'
        'Alpine Linux': 'apk list --installed',
        'openSUSE': 'zypper se -i',
        'Fedora': 'dnf list installed',
        'Manjaro': 'pacman -Q',
        'Void Linux': 'xbps-query -l',
        'cygwin': 'cygcheck -c'
    },
    'files-in-package': {
        'Debian': 'dpkg -L {0}',
        'CentOS': 'repoquery --installed -l {0}',
        'Red Hat Enterprise Linux': 'rpm -ql {0}',
        'Ubuntu': 'dpkg -L {0}',
        'Pop!_OS': 'dpkg -L {0}',
        'Arch Linux': 'pacman -Ql {0}',
        'Gentoo': 'equery files {0}',  # Part of gentoolkit
        'Alpine Linux': 'apk info -L {0}',
        'openSUSE': 'rpm -ql {0}',
        'Fedora': 'rpm -ql {0}',
        'Manjaro': 'pacman -Ql {0}',
        'Void Linux': 'xbps-query -f {0}',
        'cygwin': 'cygcheck -l {0}'
    },
    'package-info': {
        'Debian': 'aptitude show {0}',
        'CentOS': 'yum info {0}',
        'Red Hat Enterprise Linux': 'dnf info {0}',
        'Ubuntu': 'apt show {0}',
        'Pop!_OS': 'apt show {0}',
        'Arch Linux': 'pacman -Si {0}',  # -Qi for installed packages
        'Gentoo': 'emerge -pv {0}',
        'Alpine Linux': 'apk info {0}',
        'openSUSE': 'zypper info {0}',
        'Fedora': 'dnf info {0}',
        'Manjaro': 'pacman -Si {0}',  # -Qi for installed packages
        'Void Linux': 'xbps-query -f {0}',
        'cygwin': 'apt-cyg show {0}'
    }
}

current_platform = get_platform_id()

def dump():
    #return "%s\n" % yaml.dump(commands, default_flow_style=False)
    for topcmd, cmds in commands.items():
        print(topcmd)
        for plat, cmd in cmds.items():
            print("    %s: %s" % (plat, cmd))

def countargs(strng):
    'hack'
    openb=strng.count('{')
    closeb=strng.count('}')
    if closeb >= openb:
        return openb
    else:
        return 0

def get_command(cmd, *args):
    command_template=commands[cmd][current_platform]
    if countargs(command_template) > 0:
        if len(args) != countargs(command_template):
            sys.stdout.write("Wrong number of arguments: %s, should be %s\n%s" % (len(args),
                                                                                  countargs(command_template),
                                                                                  dump()))
            sys.exit()
        return command_template.format(*args)
    else:
        return command_template

def process_run(cmd_string, stdin=None):
    return subprocess.Popen(shlex.split(cmd_string),
                            stdin=stdin,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

def process_results(process_object):
    (stdout, stderr)=process_object.communicate()
    return (process_object.returncode, stdout.decode('UTF-8'), stderr.decode('UTF-8'))

def run_command(cmd, *args):
    fullcmd=get_command(cmd, *args)
    print ("#", fullcmd)
    return process_results(process_run(fullcmd))

if __name__=='__main__':
    rc, out, err = run_command(sys.argv[1], *sys.argv[2:])
    if rc == 0:
        print(out)
    else:
        print("error:", rc)
        print(err)
