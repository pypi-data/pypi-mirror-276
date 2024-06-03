from setuptools import setup, find_packages

setup(
    name="readme-ation",
    version="0.1.13",
    packages=find_packages(),
    author='Charles Feinn',
    author_email='chuckfinca@gmail.com',
    description='A README.md generation tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chuckfinca/readme-ation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'pkg_vers>=0.0.1',
    ],
    license_files = ('LICENSE.txt',),
)
