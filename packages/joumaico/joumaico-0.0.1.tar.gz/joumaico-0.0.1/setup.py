from setuptools import setup

setup(
    name="joumaico",
    version="0.0.1",
    author="Joumaico Maulas",
    description="Test Package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=['joumaico'],
    package_dir={'joumaico': 'src/joumaico'},
    package_data={'joumaico': ['data/*.txt']},
    python_requires=">=3.11",
    install_requires=[
        "aiosqlite",
    ],
)
