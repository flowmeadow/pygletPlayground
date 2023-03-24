import os

from setuptools import find_packages, setup

os.system("pip freeze > requirements.txt")
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
print(REQUIREMENTS)
setup(
    name="glpg",
    version="0.2.1",
    license="MIT",
    packages=find_packages(include=["glpg", "glpg.*"]),
    install_requires=['attrs==21.4.0', 'numpy==1.23.1', 'Pillow==9.3.0', 'pyglet==1.5.26', 'python-utils==3.4.5'],
    include_package_data=True,
    description="pyglet OpenGL playground",
    author="Florian Wiese",
    author_email="florian-wiese93@outlook.de",
    url="https://github.com/flowmeadow/pygletPlayground",
    download_url="https://github.com/flowmeadow/pygletPlayground.git",
    keywords=["pyglet", "OpenGL"],
)
