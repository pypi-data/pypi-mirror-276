

from setuptools import setup, find_packages

# Read version from the package
def get_version():
    with open('nugen/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split('=')[1].strip()[1:-1]


setup(
    name='nugen',
    version=get_version(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nugen = nugen.cli:main'
        ]
    },
    install_requires=[
        'pytz',
    ],
)

