import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uztagger",
    version="0.0.11",
    author="Ulugbek Salaev",
    author_email="ulugbek0302@gmail.com",
    description="uztagger | Uzbek Morphological Part of Speech (POS) Tagging on Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UlugbekSalaev/uztagger",
    project_urls={
        "Bug Tracker": "https://github.com/UlugbekSalaev/uztagger/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['mophology', 'uzbek-language', 'pos tagging', 'morphological tagging'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["UzMorphAnalyser", "pandas"],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["*.csv", "*.png"]},
    #package_data={"": ["cyr_exwords.csv", "lat_exwords.csv"],},
)