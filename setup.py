from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from subprocess import call
from setuptools import setup, find_packages
import pip

def custom_command():
    # pip.main(['install', package]) # for whatever reason, this command does not work
    call(['pip', 'install', 'https://github.com/vwxyzjn/histraffic/raw/master/Shapely-1.5.17-cp36-cp36m-win_amd64.whl'])
    print('hello world')

class CustomInstallCommand(install):
    def run(self):
        custom_command()
        install.run(self)


setup(
  name = 'streettraffic',
  packages = find_packages(), # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Costa Huang',
  author_email = 'Costa.Huang@outlook.com',
  install_requires = [
    'rethinkdb',
    'pandas',
    'python-dateutil',
    'requests',
    'pillow',
    'geopy',
    'matplotlib'
  ],
  cmdclass={
    'install': CustomInstallCommand
  }
)

# run python setup.py sdist for distribution.