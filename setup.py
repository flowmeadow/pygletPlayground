import os

from setuptools import find_packages, setup

os.system("pip freeze > requirements.txt")
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
print(REQUIREMENTS)
setup(
    name="glpg_flowmeadow",
    version="0.1.4",
    license="MIT",
    packages=find_packages(include=["glpg_flowmeadow", "glpg_flowmeadow.*"]),
    install_requires=[
        "attrs==21.4.0",
        "cycler==0.11.0",
        "fonttools==4.33.3",
        "kiwisolver==1.4.3",
        "numpy==1.22.3",
        "overrides==6.1.0",
        "packaging==21.3",
        "pyglet==1.5.23",
        "pyparsing==3.0.9",
        "python-dateutil==2.8.2",
        "six==1.16.0",
        "typing-utils==0.1.0",
    ],
    include_package_data=True,
    description="pyglet OpenGL playground",
    author="Florian Wiese",
    author_email="florian-wiese93@outlook.de",
    url="https://github.com/flowmeadow/pygletPlayground",
    download_url="https://github.com/flowmeadow/pygletPlayground.git",
    keywords=["pyglet", "OpenGL"],
)
