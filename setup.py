from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='reree',
    version='0.1.3',
    description='REgex Rule Entity Extractor',
    author='MJ Jang',
    install_requires=[],
    packages=find_packages(exclude=['docs', 'tests', 'tmp', 'data']),
    python_requires='>=3',
    package_data={'reree': ['resources/*']},
    zip_safe=False,
    include_package_data=True
)
