from setuptools import find_packages, setup

setup(
    name="ipc_parser",
    version="0.1.0",
    author="Shayan Sadeghi",
    author_email="ShayanSadeghi1996@gmail.com",
    description="Parsing XML International Patent Classifications (IPC)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ShayanSadeghi/ipc_parser",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "lxml",
    ],
    keywords=["ipc", "patent", "wipo"],
)
