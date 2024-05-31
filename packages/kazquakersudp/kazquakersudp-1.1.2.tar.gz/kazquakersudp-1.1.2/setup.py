import setuptools
from kazquakersudp import _version

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="kazquakersudp",
    version=_version.version,
    author="Rishat Sultanov",
    author_email="rihasultanov@gmail.com",
    license='GPLv3',
    description="Tools for receiving and interacting with Raspberry Shake UDP data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kazquake/rsudp",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['obspy', 'numpy', 'matplotlib<3.2', 'pydub', 'twython',
                      'python-telegram-bot<=13.11'],
    entry_points = {
        'console_scripts': [
            'rs-packetloss=kazquakersudp.packetloss:main',
            'rs-client=kazquakersudp.client:main',
            'rs-test=kazquakersudp.client:test',
            'packetize=kazquakersudp.packetize:main',
            'rs-settings=kazquakersudp.entry_points:ep_edit_settings',
            'rs-log=kazquakersudp.entry_points:ep_cat_log',
            'rs-tailf=kazquakersudp.entry_points:ep_tailf_log',
            ],
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Framework :: Matplotlib",
        "Topic :: Scientific/Engineering :: Physics",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Development Status :: 5 - Production/Stable",
    ],
)
