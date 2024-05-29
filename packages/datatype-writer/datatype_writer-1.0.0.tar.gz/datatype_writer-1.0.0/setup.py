from setuptools import setup

VERSION = '1.0.0'
DESCRIPTION = 'Framework for writing binary data in python'
LONG_DESCRIPTION = 'Framework that allows the use of operatators, such as & or |, for chaining different datatypes together and allowing for easy writing.'

setup(
    name="datatype_writer",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    author="Ada L",
    author_email="the.nostra.tymus@gmail.com",
    license='MIT',
    packages=['datatype_writer'],
    install_requires=[
        'pyyaml',
    ],
    keywords='machine learning',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
)
