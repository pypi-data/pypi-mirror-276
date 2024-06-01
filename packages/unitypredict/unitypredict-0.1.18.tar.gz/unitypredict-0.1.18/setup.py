from setuptools import setup, find_packages

description = ""
with open("README.md", "r") as rdf:
    description = rdf.read()

print ("Possible packages: {}".format(find_packages()))

setup (
    name="unitypredict",
    version="0.1.18",
    packages=find_packages(),
    install_requires=[
        # Currently no dependencies
    ],
    entry_points = {          # this here is the magic that binds your function into a callable script
        'console_scripts': 
        [
            'uptools=unitypredict.scripts:main'
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown"
)
