from setuptools import setup, find_packages
import re
import os


PACKAGE_DIR = os.path.join(os.getcwd(), 'grain_zip_deployer')
with open(os.path.join(PACKAGE_DIR, 'version.py')) as version_file:
    verstrline = version_file.read().strip()
VSRE = r'^__version__ = [\']([0-9\.]*)[\']'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    VERSION = mo.group(1)
else:
    raise Exception('No version string found')


with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='grain_zip_deployer',
    version=VERSION,
    entry_points={
        'console_scripts': [
            'grain_upload_zip = grain_zip_deployer.main:main',
        ],
    },
    description='Used to upload sourcecode as zip-file to a cloud storage bucket',
    license='MIT',
    packages=find_packages(),
    author='Jacob Noordmans',
    author_email='jacob@graindataconsultants.com',
    keywords=['Zip','Cloud storage']
)

install_requires = [
    'google-cloud-storage==2.16.0',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)