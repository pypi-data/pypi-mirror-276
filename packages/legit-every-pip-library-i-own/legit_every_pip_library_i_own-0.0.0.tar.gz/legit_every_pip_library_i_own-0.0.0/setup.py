from setuptools import setup, find_packages

setup(
    name="legit_every_pip_library_i_own",
    packages=find_packages(),
    install_requires=[],
    author="restriction policy happend",
    author_email="zaksteryt@gmail.com",
    description="import literraly every pip library you own",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
