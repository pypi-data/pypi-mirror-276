from setuptools import setup, find_packages

setup(
    name="YWP",
    version="0.7.0",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition",
        "gtts",
        "pygame",
        "sounddevice",
        "pyaudio"
    ],
    package_data={
        '': ['aimp.exe'],  # Include aimp.exe at the root level of the package
    },
    data_files=[('', ['aimp.exe'])],  # Another way to include aimp.exe
    entry_points={
        'console_scripts': [
            'YWP_install_AIMP = YWP:AIMP_Run', 
        ],
    },
    author="Your Wanted Products",
    author_email="pbstzidr@ywp.freewebhostmost.com",
    description="A big Package has a lot of things",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/YourWantedProducts/YWP_Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)