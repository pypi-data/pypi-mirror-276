import json

from setuptools import setup

setup(
    name="osstrack",
    description="Manage uploads to osstrack.io.",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    author="The OSSTrack Team",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
    version=json.load(open("package.json"))["version"],
    packages=[],
    scripts=["osstrack"],
)
