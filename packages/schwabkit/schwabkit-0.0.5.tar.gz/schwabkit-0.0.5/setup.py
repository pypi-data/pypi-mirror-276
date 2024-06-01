from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Schwab API Python Client (unofficial)'
LONG_DESCRIPTION = 'This is an unofficial python program to access the Schwab api.'

setup(
    name='schwabkit',
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