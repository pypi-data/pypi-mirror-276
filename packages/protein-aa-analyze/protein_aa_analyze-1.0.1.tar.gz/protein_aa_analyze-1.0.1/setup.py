from setuptools import setup, find_packages

setup(
    name="protein_aa_analyze",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'protein_aa_analyze=protein_aa_analyze.analyzer:main',
        ],
    },
    author="Iman Jouiad",
    author_email="iman.jouiad@gmail.com",
    description="A simple Protein Amino-Acid Analyzer CLI application",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Imanjdd/protein_aa_analyze.git",
    license= "OSI Approved :: MIT License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)