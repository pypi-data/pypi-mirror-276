from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Schwab API Python Client (unofficial)'
with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='schwab-dev',
    version=VERSION,
    author='Tyler Bowers',
    author_email='tylerebowers@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
        'websockets',
    ],
    keywords=['python', 'schwab', 'api', 'client'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)