from setuptools import setup, find_packages

VERSION = '1.1.0'
DESCRIPTION = 'Time series utility package'

# Setting up
setup(
    name="kaal",
    version=VERSION,
    author="Debangan Mishra",
    author_email="debangan.coding@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'time series', 'time analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Data Scientists",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)