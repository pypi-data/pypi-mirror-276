from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='liteium',
    version='1.0.5',
    description='Description of your package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='El Bettioui Reda',
    author_email='redaelbettioui@gmail.com',
    url='https://github.com/XredaX/liteium',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
