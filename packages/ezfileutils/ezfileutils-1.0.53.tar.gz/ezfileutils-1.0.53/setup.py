from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ezfileutils',
    version='1.0.53',
    description='A Python utility script for common file operations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='subbsandwich',
    author_email='tanagitanagiakori@gmail.com',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ezfileutils=ezfileutils:main'
        ]
    },
)
