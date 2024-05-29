import pathlib
import setuptools

setuptools.setup(
	name ="BISOInvest_data",
	version = "0.1.0",
	description = "Brief description",
	long_description = pathlib.Path("README.md").read_text(),
	long_description_content_type = "text/markdown",
	#url = "home_link",
	author = "Oliver Ekeberg",
	author_email = "ekebergoliver@gmail.com",
	license = "The Unlicense",
	# project_urls = {
	# "Documentation" : "",
	# "Source" : ""
	# },
	classifiers = [
	"Development Status :: 1 - Planning",
	"Development Status :: 4 - Beta",
	"Programming Language :: Python :: 3.10",
	"Programming Language :: Python :: 3.11",
	"Programming Language :: Python :: 3.12",
	"License :: OSI Approved :: MIT License"
	],
	python_requires = ">=3.10",
	install_requires = ["requests", "pandas>=2.0", "numpy>=1.0"],
	extras_require = {
	"excel": ["openpyxl"]
	},
	packages = setuptools.find_packages(),
	include_package_data = True,
	entry_points = {"console_scripts": ["BISOInvest = BISOInvest.cli:main"]},
	)