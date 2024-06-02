from setuptools import setup, find_packages

setup(
    name='graphmemory',
    version='0.1.1',
    author='BradAGI',
    author_email='cavemen_summary_0f@icloud.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/graphmemory/',
    license='LICENSE.txt',
    description='A package for creating a graph database for use with GraphRAG.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'duckdb',
        'pydantic'
    ],
    keywords='graphrag graph database rag'
)
