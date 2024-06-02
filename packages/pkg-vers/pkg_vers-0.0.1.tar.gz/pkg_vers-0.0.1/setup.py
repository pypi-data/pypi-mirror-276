from setuptools import setup, find_packages

setup(
    name="pkg_vers",
    version="0.0.1",
    packages=find_packages(),
    author='Charles Feinn',
    author_email='chuckfinca@gmail.com',
    description="pkg_vers is a utility to determine versions of top-level packages used in your project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chuckfinca/mod_vers',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    license_files = ('LICENSE.txt',),
)
