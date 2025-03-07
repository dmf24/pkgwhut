import platform
import sys
import os

def get_platform_id():
    """
    Returns 'cygwin' if running on Cygwin, or the Linux distribution name if on Linux.
    For other platforms (e.g., Windows, macOS), returns the system name.
    Compatible with Python 3.6+.
    """
    # Check for Cygwin first
    if sys.platform == 'cygwin' or 'CYGWIN' in platform.system():
        return 'cygwin'

    # Handle Linux
    if sys.platform.startswith('linux'):
        # Try /etc/os-release (modern standard)
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
            distro_info = {}
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    distro_info[key] = value.strip('"')
            # Return NAME field, similar to platform.linux_distribution()[0]
            return distro_info.get('NAME', 'Linux')
        
        # Fallback to older /etc/*-release files
        release_files = [
            '/etc/redhat-release',
            '/etc/debian_version',
            '/etc/lsb-release'
        ]
        for release_file in release_files:
            if os.path.exists(release_file):
                with open(release_file, 'r') as f:
                    content = f.read().strip()
                if 'redhat' in release_file.lower():
                    if 'Red Hat' in content:
                        return 'Red Hat Enterprise Linux'
                    elif 'CentOS' in content:
                        return 'CentOS'
                elif 'debian' in release_file.lower():
                    return 'Debian'
                elif 'lsb-release' in release_file:
                    with open(release_file, 'r') as lsb_f:
                        for line in lsb_f:
                            if line.startswith('DISTRIB_ID='):
                                return line.split('=', 1)[1].strip()
        return 'Linux'  # Generic fallback

    # For non-Linux, non-Cygwin (e.g., Windows, macOS)
    return platform.system()


# Example usage
if __name__ == "__main__":
    print(get_platform_id())
