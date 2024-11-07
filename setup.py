import setuptools
from setuptools_scm import get_version

version = get_version(root=".", relative_to=__file__)

setuptools.setup(
    name="logging-by-oriash",
    version=version,
    author="oriash93",
    description="Custom Python logging library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oriash93/logging-utils",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    setup_requires=["setuptools>=64", "setuptools_scm>=8"],
    use_scm_version=True,
    include_package_data=True,
    zip_safe=False,
)
