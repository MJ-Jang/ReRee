from setuptools import setup, find_packages

setup(
    name='reree',
    version='0.1',
    description='REgex Rule Entity Extractor',
    author='MJ Jang',
    install_requires=[],
    packages=find_packages(exclude=['docs', 'tests', 'tmp']),
    python_requires='>=3',
    zip_safe=False,
    include_package_data=True
)
