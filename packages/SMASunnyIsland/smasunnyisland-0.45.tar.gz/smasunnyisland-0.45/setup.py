from setuptools import setup, find_packages

setup(
    name='smasunnyisland',
    version='1.42',    
    description='Python package to read and control SMA Sunny Island inverters',
    url='https://github.com/HarmvandenBrink/SMA_Sunny_Island_Controller',
    author='Harm van den Brink',
    author_email='harmvandenbrink@gmail.com',
    packages=['smasunnyisland'],
    install_requires=['pyserial', 'pymodbus==2.5.3', 'pysunspec==2.1.1'],

    classifiers=[
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ]
)