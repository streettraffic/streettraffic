from setuptools.command.install import install
from wheel.bdist_wheel import bdist_wheel
from subprocess import call
from setuptools import setup, find_packages
import platform
import pip

def custom_command():
    # pip.main(['install', package]) # for whatever reason, this command does not work
    if platform.system() == 'Windows':
        ## windows apparently is a little special, we have to install shapely through
        ## http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
        if platform.architecture()[0] == '64bit':
            call(['pip', 'install', 'https://github.com/streettraffic/streettraffic.github.io/raw/master/assets/Shapely-1.5.17-cp36-cp36m-win_amd64.whl'])
        else:
            call(['pip', 'install', 'https://github.com/streettraffic/streettraffic.github.io/raw/master/assets/Shapely-1.5.17-cp36-cp36m-win32.whl'])
    else:
        call(['pip', 'install', 'shapely'])

class CustomInstallCommand(install):
    def run(self):
        custom_command()
        install.run(self)

class Custom_bdist_wheel(bdist_wheel):
    def run(self):
        custom_command()
        bdist_wheel.run(self)


setup(
    name = 'streettraffic',
    packages = find_packages(), # this must be the same as the name above
    version = '0.2.0',
    description = 'Monitor the traffic flow of your favorite routes, cities, and more',
    url='https://github.com/vwxyzjn/streettraffic',
    author = 'Costa Huang',
    author_email = 'Costa.Huang@outlook.com',
    python_requires='>=3.6',
    include_package_data = True,
    install_requires = [
        'rethinkdb',
        'pandas',
        'python-dateutil',
        'requests',
        'pillow',
        'geopy',
        'matplotlib',
        'websockets',
        'sphinxcontrib-napoleon'
    ],
    cmdclass={
        'install': CustomInstallCommand,
        'bdist_wheel': Custom_bdist_wheel
    }
)

# run python setup.py sdist for distribution.