from setuptools import setup, find_packages

setup(
    name="MIScikit-Learn",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
        ],
    },
    author="Mohieddine Farid | Imane Fjer",
    author_email="farid.mohieddine@um6p.ma | imane.fjer@um6p.ma",
    description="A lightweight machine learning library inspired by scikit-learn.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/MohiZzine/mini-scikit-learn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
