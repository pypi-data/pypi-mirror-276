from setuptools import setup, find_packages


setup(
    name="walletAVA",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "web3",
        "cryptography",
        "pathlib",
        "requests"
    ],
    author="kikakop",
    author_email="kikakopjunior@gmail.com",
    description="Module gestion wallet basee sur la blockchain ethereurm",
    long_description_content_type='text/markdown',
    url="https://gitlab.com/kikakopjunior/walletweb3.git",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)