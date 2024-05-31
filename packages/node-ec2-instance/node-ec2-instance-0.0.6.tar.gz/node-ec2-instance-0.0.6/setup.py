import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "node-ec2-instance",
    "version": "0.0.6",
    "description": "CDK construct library for creating an EC2 instance with Node.js installed",
    "license": "Apache-2.0",
    "url": "https://github.com/badmintoncryer/cdk-node-ec2-instance.git",
    "long_description_content_type": "text/markdown",
    "author": "Kazuho CryerShinozuka<malaysia.cryer@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/badmintoncryer/cdk-node-ec2-instance.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "node_ec2_instance",
        "node_ec2_instance._jsii"
    ],
    "package_data": {
        "node_ec2_instance._jsii": [
            "cdk-node-ec2-instance@0.0.6.jsii.tgz"
        ],
        "node_ec2_instance": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.143.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.98.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
