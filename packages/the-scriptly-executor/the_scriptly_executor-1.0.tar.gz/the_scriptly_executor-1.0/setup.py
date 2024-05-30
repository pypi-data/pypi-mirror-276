from setuptools import setup, find_packages

requirements = [line.strip() for line in open("requirements.txt").readlines()]

setup(
    name="the-scriptly-executor",
    version="1.0",
    author="gabrg4",
    author_email="gabriele.goffredo.06+pypi@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    keywords=["python", "discord", "scriptly", "speech recognition", "speech to text", "stt"],
)
