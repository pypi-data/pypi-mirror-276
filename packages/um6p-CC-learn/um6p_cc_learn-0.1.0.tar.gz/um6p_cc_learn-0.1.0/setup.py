from setuptools import setup, find_packages

setup(
    name="um6p_CC_learn",
    version="0.1.0",
    author="Sami AGOURRAM , Ilyass Hakkou",
    author_email="Sami.AGOURRAM@um6p.ma",
    description="A home made sklearn",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "scikit-learn>=0.24.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
