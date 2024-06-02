from setuptools import setup, find_packages

setup(
    name='sidcli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
    ],
    entry_points='''
        [console_scripts]
        sid=sidcli.sidcli:sidcli
    ''',
)
