from setuptools import setup, find_packages

setup(
    name="YWP",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition",
        "gtts",
        "pygame",
        "sounddevice",
        "pyaudio"
    ],
    author="Your Wanted Products",
    author_email="pbstzidr@ywp.freewebhostmost.com",
    description="A big Package has a lot of things",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YourWantedProducts/YWP_Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
