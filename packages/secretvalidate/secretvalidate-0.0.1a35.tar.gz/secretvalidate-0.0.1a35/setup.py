from setuptools import setup, find_packages
import os

# Get the path to requirements.txt which is one folder up
requirements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'requirements.txt'))

# Read requirements from requirements.txt
with open(requirements_path, 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='secretvalidate',
    version='0.0.1a35',
    description='A cli/package for validating secrets.',
    author='VigneshKna',
    author_email='Vkna@email.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt', '../requirements.txt', '../urls.json'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'secretvalidate=secretvalidate.validator:main',
        ],
    },
)
