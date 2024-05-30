from setuptools import setup, find_packages

setup(
    name="entoli",
    version="0.1.0",
    author="Your Name",
    author_email="cwahn0904@gmail.com",
    description="A Python functional programming library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cwahn/entoli",  # Update this URL to your project's repository
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        "attrs==23.2.0",
        "distlib==0.3.8",
        "filelock==3.14.0",
        "iniconfig==2.0.0",
        "more-itertools==10.2.0",
        "packaging==24.0",
        "platformdirs==4.2.2",
        "pluggy==0.13.1",
        "py==1.11.0",
        "toml==0.10.2",
        "virtualenv==20.26.2",
        "wheel==0.33.6",
    ],
    extras_require={
        "dev": open("requirements_dev.txt").read().splitlines(),
    },
    entry_points={
        "console_scripts": [
            # Add any CLI scripts here
        ],
    },
)
