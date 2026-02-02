from setuptools import setup, find_packages

setup(
    name="omni-os",
    version="0.1.0",
    description="The Universal Runtime for Autonomous Intelligence",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aurelius Systems",
    author_email="system@aurelius.ai",
    url="https://github.com/aurelius/omni",
    py_modules=["omni"],
    install_requires=[
        "typer",
        "rich",
        "llama-cpp-python",
        "requests",
        "pydantic"
    ],
    entry_points={
        "console_scripts": [
            "omni=omni:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
