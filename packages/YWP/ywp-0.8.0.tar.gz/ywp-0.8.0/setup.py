import os
from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

# class CustomInstallCommand(InstallCommand):
#     def run(self):
#         # Download the required file from a URL
#         url = 'https://example.com/aimp.exe'
#         os.system(f'curl -o aimp.exe {url}')  # Use appropriate command for downloading

#         # Continue with the regular installation process
#         super().run()

setup(
    name="YWP",
    version="0.8.0",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition",
        "gtts",
        "pygame",
        "sounddevice",
        "pyaudio"
    ],
    # package_data={
    #     '': ['aimp.exe'],  # Include aimp.exe at the root level of the package
    # },
    # data_files=[('', ['aimp.exe'])],  # Another way to include aimp.exe
    # entry_points={
    #     'console_scripts': [
    #         'YWP_install_AIMP = YWP:AIMP_Run', 
    #     ],
    # },
    author="Your Wanted Products",
    author_email="pbstzidr@ywp.freewebhostmost.com",
    description="A big Package has a lot of things",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/YourWantedProducts/YWP_Python",
    # cmdclass={
    #     'install': CustomInstallCommand,
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)