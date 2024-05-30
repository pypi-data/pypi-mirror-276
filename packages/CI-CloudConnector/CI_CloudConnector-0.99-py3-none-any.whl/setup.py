import logic
from distutils.core import setup
from setuptools import setup, find_packages

def getVersion():
    ans = ""
    try:
        ans = logic.getLocalVersion()
    except Exception as inst:
        print("Error getting version") + str(inst)

    return ans



setup(
    name="CI_CloudConnector",
    version="0.99",
    packages=find_packages(),
    py_modules=["logic", "main", "setup", "myservice"],
    description="IOT application that collects data from PLC (ModBus or AnB Ethernet/IP) and sends it to the cloud using HTTPS",
    author="Yochai",
    author_email="yochaim@contel.co.il",
    install_requires=[],
    url="https://trunovate.com/",
    long_description=open("README.txt").read()  # Make sure you have README.txt in the same directory
)