from setuptools import setup

with open("README.rst", "rb") as f:
    long_description = f.read()

setup(
  name = 'altseeker',
  packages=['altseeker'],
  version = '1.0',
  scripts=['altseeker/altseeker'],
  description = "Uses deep learning to caption img tags within a web page and fills out their alt attribute with the related caption",
  long_description=long_description,
  author = 'Karamjeet Singh',
  author_email = 'karamjeetsinghgulati111@gmail.com',
  url = 'https://github.com/ksg98/altseeker',
  #download_url = 'https://github.com/ksg98/altseeker/tarball/3.3',
  keywords = ['alt', 'caption', 'images', 'deep learning'], # arbitrary keywords
  classifiers = [],
  install_requires = ['beautifulsoup4', 'html5lib'],
  license="Apache-2.0"
)
