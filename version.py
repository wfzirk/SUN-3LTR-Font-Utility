# Source: https://github.com/Changaco/version.py

from os.path import dirname, isdir, join
import re
from subprocess import CalledProcessError, check_output

PREFIX = ''

tag_re = re.compile(r'\btag: %s([0-9][^,]*)\b' % PREFIX)
version_re = re.compile('^Version: (.+)$', re.M)


def get_version():
    # Return the version if it has been injected into the file by git-archive
    version = tag_re.search('$Format:%D$')
    #print('v1',version)
    if version:
        #print('vg',version)
        return version.group(1)

    d = dirname(__file__)

    if isdir(join(d, '.git')):
        # Get the version using "git describe".
        #cmd = 'git describe --tags --match %s[0-9]* --dirty' % PREFIX
        cmd = 'git describe --tags'
        try:
            version = check_output(cmd.split()).decode().strip()[len(PREFIX):]
        except CalledProcessError:
            raise RuntimeError('Unable to get version number from git tags')

        # PEP 440 compatibility
        if '-' in version:
            if version.endswith('-dirty'):
                raise RuntimeError('The working tree is dirty')
            version = version.split('-')[0]
        with open('version.ini', 'w') as f:
            f.write(version)
            #print('w',version)
    else:
         with open('version.ini') as f:
            version = f.read()
            #print('r',version)
    #print('ret',version)
    return version


if __name__ == '__main__':
    print(get_version())