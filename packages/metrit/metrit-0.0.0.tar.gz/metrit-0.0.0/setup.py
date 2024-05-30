from setuptools import setup

# version = "{{VERSION_PLACEHOLDER}}"
setup(
    name="metrit",
    use_scm_version=True,
    author="mcrespoae",
    author_email="info@mariocrespo.es",
    packages=["metrit"],
    description="A dead simple resources monitoring decorator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mcrespoae/metrit",
    install_requires=["psutil==5.9.8", "multiprocess==0.70.16"],
    setup_requires=["psutil==5.9.8", "multiprocess==0.70.16"],
    python_requires=">=3.8",
    keywords=["metrit"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
