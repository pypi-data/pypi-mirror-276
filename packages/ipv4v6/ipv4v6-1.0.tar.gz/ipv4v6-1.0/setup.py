from setuptools import setup, find_packages
VERSION = '1.0'
DESCRIPTION = 'A model for get ipv4&ipv6 address'
LONG_DESCRIPTION = '''This is a model to get your ip address.
Usage: get_ip() is used to get your ipv4 address including host and port.(You can give a specific socket as parameter)
       get_ipv4() is used to get your ipv4 address including only host.
       (Tips: If you just want to get ipv4 address, get_ip() is a better choice.)
       ip_tuple() returns a tuple of the host and port of your ipv4 address.
       (Tips: ip_tuple() can be given to socket.connect() as parameter.)
       get_ipv6() is used to get your ipv6 address including only host.
       get_ipv4_location() is used to get the location of your ipv4 address.
       get_ipv6_location() is used to get the location of your ipv6 address.'''
setup(
    name="ipv4v6",
    version=VERSION,
    author="OscarMYH(myhldh)",
    author_email='oscarmyh@163.com',
    url='https://github.com/myhldh/GetIP',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['python','computer vision','OscarMYH','myhldh','lightweight','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)