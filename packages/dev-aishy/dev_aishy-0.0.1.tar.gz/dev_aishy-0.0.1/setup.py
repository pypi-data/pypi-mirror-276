from setuptools import setup, find_packages

setup(
    name='dev_aishy',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aishy = dev_aishy:testing.hello_class"
        ]
    },
    install_requires=[]
)