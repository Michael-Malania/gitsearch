from setuptools import setup, find_packages

setup(
    name='gitsearch',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['click', 'requests', 'blessed','texttable'],
    entry_points='''
    [console_scripts]
    gitsearch=gitsearch:searcher
    '''
)