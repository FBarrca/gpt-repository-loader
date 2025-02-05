from setuptools import setup, find_packages

setup(
    name="gpt-repository-loader",
    version="0.1.0",
    author="mpoon & FBarrca",
    author_email="your.email@example.com",
    description="A tool to convert Git repository contents into AI-friendly text format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fbarrca/gpt-repository-loader",
    license="MIT",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "gpt-repository-loader=gpt_repository_loader.cli:main_cli",
            "gpt-repository-loader.exe=gpt_repository_loader.cli:main_cli",  # Windows Support
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
