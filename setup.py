from setuptools.command.install import install
from wheel.bdist_wheel import bdist_wheel
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

class Custom_bdist_wheel(bdist_wheel):
    def run(self):
        custom_command()
        bdist_wheel.run(self)


setup(
    name = 'streettraffic',
    packages = find_packages(), # this must be the same as the name above
    version = '0.1.3',
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