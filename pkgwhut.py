HTTP/1.1 200 OK
date: Fri, 07 Mar 2025 16:36:15 GMT
server: Apache
last-modified: Fri, 07 Mar 2025 16:34:59 GMT
etag: "b3c-62fc3341846ab"
accept-ranges: bytes
content-length: 2876
webconf2: rccg-sandbox-dev01.rc.hms.harvard.edu
strict-transport-security: max-age=15768000

import sys,os
import platform
from scripting import process
#import yaml

commands={'which-package-has-file': {'debian': 'dpkg --search {0}',
                                     'CentOS': 'repoquery --installed -f {0}',
                                     'CentOS Linux': 'repoquery --installed -f {0}',
                                     'Red Hat Enterprise Linux': 'dnf repoquery --installed --file {0}'
                                     },
          'installed-packages': {'debian': 'dpkg -l',
                                 'CentOS': 'yum list installed',
                                 'CentOS Linux': 'yum list installed',
                                 'Red Hat Enterprise Linux': 'dnf list installed'
                                 },
          'files-in-package': {'debian': 'dpkg -L {0}',
                               'CentOS': 'repoquery --installed -l {0}',
                               'CentOS Linux': 'repoquery --installed -l {0}',
                               },
          'package-info': {'debian': 'aptitude show {0}',
                           'CentOS': 'yum info {0}',
                           'CentOS Linux': 'yum info {0}'
                           }}

#commands=yaml.load("""---
#cmds:
#  files-in-package:
#    CentOS: 'repoquery --installed -l {0}'
#    debian: 'dpkg -L {0}'
#  which-package-has-file:
#    CentOS: 'repoquery --installed -f {0}'
#    debian: 'dpkg --search {0}'
#  installed-packages:
#    CentOS: 'yum list installed'
#    debian: 'dpkg -l'
#  package-info:
#    CentOS: 'yum info {0}'
#    debian: 'aptitude show {0}'
#""")['cmds']
try:
    current_platform = platform.linux_distribution()[0]
except AttributeError:
    import distro
    current_platform = distro.linux_distribution()[0]

def dump():
    return "%s\n" % yaml.dump(commands, default_flow_style=False)

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

def run_command(cmd, *args):
    fullcmd=get_command(cmd, *args)
    print ("#", fullcmd)
    return process(fullcmd)

if __name__=='__main__':
    rc, out, err = run_command(sys.argv[1], *sys.argv[2:])
    if rc == 0:
        print(out)
    else:
        print("error:", rc)
        print(err)
