from setuptools import setup, find_packages

setup(
    name="hashsan-tool",  
    version="0.1.1",
    packages=find_packages(),
    description="A tool for retrieving original text from encrypted or locked text using a wordlist.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="X-Projetion",
    author_email="lutfifakee@proton.me",
    url="https://github.com/X-Projetion/hashsan",
    project_urls={
        "Documentation": "https://github.com/X-Projetion/hashsan/wiki",
        "Source Code": "https://github.com/X-Projetion/hashsan",
        "Bug Tracker": "https://github.com/X-Projetion/hashsan/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    keywords="hash lookup MD5 cryptography security",
    python_requires='>=3.6',
    install_requires=[
        "dependency1",
        "dependency2",
    ],
    entry_points={
        'console_scripts': [
            'hashsan=hashsan:main',
        ],
    },
)
