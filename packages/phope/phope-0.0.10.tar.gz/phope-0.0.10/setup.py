import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phope",
    version="0.0.10",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="universal biomarker prediction tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/patient",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/patient",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['phope'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'phope = phope:main'
        ]
    },
)
