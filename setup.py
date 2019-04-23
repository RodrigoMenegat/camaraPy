import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="camaraPy",
	version="0.0.4",
	author="Rodrigo Menegat Schuinski",
	author_email="rodrigoschuinski@gmail.com",
	description="A wrapper for the Brazilian House of Representatives public data API",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/RodrigoMenegat/camaraPy",
	packages=setuptools.find_packages(),
  python_requires=">=3.6",
  install_requires = [
		"requests>=2.21.0",
		"xmltodict>=0.12.0",
],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Operating System :: Unix",
	]
)
