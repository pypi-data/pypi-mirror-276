from setuptools import setup, find_packages

setup(
    name='plutocontrol',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Saail Chavan',
    author_email='saailchavan02@gmail.com',
    description='A library for controlling Pluto drones',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DronaAviation/plutocontrol.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
