from setuptools import setup, find_packages
from pathlib import Path

setup(
    name= 'pro-video-ferramentas-gutierri',
    version= 1.0,
    description= 'Este pacote irá fornecer ferramentas de processamento de video ',
    long_description= Path('README.md').read_text(),
    author= 'Allef gutierri',
    author_email= 'allef@yahoo.com',
    keywords= ['camera', 'processamento', 'video'],
    packages= find_packages()
)