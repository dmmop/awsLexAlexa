from distutils.core import setup

setup(
    name='AWSLexAlexa',
    version='0.1dev',
    author="David Martinez Martin",
    author_email="davidmtn@gmail.com",
    packages=['awsLexAlexa', 'awsLexAlexa.events', 'awsLexAlexa.responses'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
