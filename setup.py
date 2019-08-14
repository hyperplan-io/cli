import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hyperplan-cli',  
    version='0.0.1-rc2',
    author="Antoine Sauray",
    author_email="antoine@hyperplan.io",
    description="A Hyperplan cli tool to help you manage your Hyperplan server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperplan/cli",
    package_dir={'': '.'},
    packages=setuptools.find_namespace_packages(where='.'),
    entry_points= {
        'console_scripts': [
            'hyperplan = hyperplan:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
)
