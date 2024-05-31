from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name="syrabrox_errorviewer",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "syrabrox-errorviewer = syrabrox_errorviewer:errorlaw",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
