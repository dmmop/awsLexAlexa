import setuptools

setuptools.setup(
    name='awsLexAlexa',
    version='0.9',
    author="David Martinez Martin",
    author_email="davidmtn@gmail.com",
    url="https://github.com/dmmop/awsLexAlexa",
    packages=['awsLexAlexa', 'awsLexAlexa/events', 'awsLexAlexa/logs'],
    # exclude=['test'],
    # include_package_data=True,
    license='GNU General Public License v3',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
