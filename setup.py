from setuptools import setup, find_packages

setup(
    name="cli-ai-assist",
    version="0.1.5",
    description="An AI companion to translate human language to command-line instructions.",
    author="RB916120",
    author_email="info@mocsctf.com",
    packages=find_packages(),
    install_requires=[
        "openai>=1.72.0",
        "python-dotenv>=0.9.9",
    ],
    entry_points={
        "console_scripts": [
            "ai=cli_AI_assist:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
