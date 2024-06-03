import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="requestweb",                     # This is the name of the package
    version="1.0.1",                        # The initial release version
    author="Abhiram.B",                     # Full name of the author
    author_email="to@abhiram.email",
    description="Fastest Way to request to send HTTP/1.1 requests extremely easily also able to enable javascript for pageload and capture html code",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',  
    license='MIT',              # Minimum version requirement of the package
    py_modules=["requestweb"],             # Name of the python package
    package_dir={'':'requestweb/src'},     # Directory of the source code of the package
    install_requires=[
        'PyQt5',
        'PyQtWebEngine',
        'beautifulsoup4',
        'python-whois',
        'requests'
    ] # Install other dependencies if any
)