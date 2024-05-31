from setuptools import find_packages, setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='userinfo',
    packages=find_packages(),
    version='1.0.0',
    author='voxj.',
    description='Get placeholder user information on python3!',
    install_requires=[],
    url='https://github.com/voxj/userinfo/',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
