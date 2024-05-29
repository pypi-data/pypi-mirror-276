# setup.py

from setuptools import setup, find_packages

setup(
    name="ma_confluence_cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "atlassian-python-api",
        "pyfunctional",
    ],
    entry_points={
        'console_scripts': [
            'ConfluenceCli=ma_confluence_cli.confluence_cli:ConfluenceCli',
        ],
    },
    author="yue.shao",
    author_email="yue.shao@dfc.sh",
    description="MA confluence automation helper",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="http://git.dfc.sh/luoshu.ma/unimarketaccessconf/-/tree/master/confluence",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
