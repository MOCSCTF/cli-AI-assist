from setuptools import setup

setup(
    name="cli-AI-assist",
    version="0.1.6",
    py_modules=["cli_AI_assist"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ai=cli_AI_assist:main",
        ],
    },
)
