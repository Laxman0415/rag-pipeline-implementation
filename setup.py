# setup.py

"""
What is setup.py?

    - setup.py is a Python script used for packaging projects. 
    - It contains metadata about your project and instructions for installing it. 
    - It's the standard file used by setuptools to distribute Python packages.

Why We Use setup.py

We use setup.py to:

    - Define metadata: name, version, author, license, etc.
    - Declare dependencies that are required (install_requires).
    - Create distributable packages (like .whl or .tar.gz).
    - Upload projects to PyPI.
    - Provide entry points for CLI tools.
    - Customize build steps or include additional data files.

Placement of setup.py

    my_project/
    ├── my_module/
    │   ├── __init__.py
    │   └── core.py
    ├── setup.py
    ├── requirements.txt
    └── README.md


Explnation:

| Field              | Purpose                                   |
| ------------------ | ----------------------------------------- |
| `name`             | Name of the package as it appears on PyPI |
| `version`          | Follows [semver](https://semver.org)      |
| `packages`         | Lists modules/submodules for packaging    |
| `install_requires` | Specifies dependencies                    |


Semantic Versioning 2.0.0

Given a version number MAJOR.MINOR.PATCH, increment the:

    - MAJOR version when you make incompatible API changes
    - MINOR version when you add functionality in a backward compatible manner
    - PATCH version when you make backward compatible bug fixes
    - Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

"""

from setuptools import setup, find_packages

setup(
    name='rag-pipeline-implementation',                                     # Package name
    version='0.0.1',                                                        # Initial version , It Follows Semantic Versioning
    description='A Package for End to End RAG Pipeline Implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Laxman Singh',
    author_email='singhlaxmandd@gmail.com',
    url='https://github.com/Laxman0415/rag-pipeline-implementation',
    license='MIT',
    packages=find_packages(exclude=["tests*"]),                             # Automatically find all packages
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.12',
    install_requires=[                                                      # Required dependencies
    ],
    entry_points={
        'console_scripts': [
            'awesome-cli=awesome_package.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],
    },
    zip_safe=False,
)