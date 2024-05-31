from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name="syrabrox",
    version="1.0.0",
    packages=find_packages(),
    url='https://github.com/syrabrox/syrabrox',
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "syrabrox = syrabrox:error",
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
