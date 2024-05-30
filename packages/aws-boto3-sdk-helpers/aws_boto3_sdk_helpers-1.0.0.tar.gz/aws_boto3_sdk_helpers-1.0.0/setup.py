from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aws-boto3-sdk-helpers',
    version='1.0.0',
    description='Contains helper functions that rely on the aws python sdk (Boto3)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='yiskaneto',
    # author_email='foo@foo.local',
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3',
        'botocore'
    ],
    license='MIT'
)
