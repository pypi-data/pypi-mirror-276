from setuptools import setup, find_packages

with open("README.md", 'r') as file:
	long_description = file.read()

setup(
	name="pypitests",
	version="0.0.12",
	description="pypitests for testing pypi services.",
	packages=find_packages(),
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/droxberka/pypitests",
	author="droxberka",
	author_email="droxberka@gmail.com",
	license="MIT",
	classifiers=[
		"License :: OSI Approved :: MIT License",
	],
	install_requires=[],
	extras_require={},
	python_requires=">=3.10",
)
