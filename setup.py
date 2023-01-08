import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dcpAlive",
    version="1.0.0",
    author="Tim Green",
    author_email="the.green.timtam@gmail.com",
    description="DCP-o-Matic with Progress Bars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thegreentimtam/dcpAlive",
    packages=setuptools.find_packages(),
    install_requires  = ['alive_progress', 'ffAlive'],
    license = 'MIT'
)
