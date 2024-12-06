from setuptools import setup, find_packages

setup(
    name="messaging-sdk",
    version="2.1.0",
    description="A Python SDK for managing messages and contacts, with webhook integration.",
    author="Amirul Islam",
    author_email="amirulislamalmamun@gmail.com",
    url="https://github.com/your-repo/messaging-sdk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "python-dotenv",
        "pytest",
        "pytest-mock",
        "flake8",
        "black",
        "mypy",
        "pydantic",
        "pytest-cov",
        "fastapi",
        "uvicorn",
        "pytest-asyncio",
        "httpx",
        "pydantic-settings",
    ],
    extras_require={
        "dev": [
            "flake8",
            "black",
            "mypy",
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "pytest-mock",
        ],
    },
    entry_points={
        "console_scripts": [
            # Example entry point (if applicable)
            # "messaging-sdk-cli = messaging_sdk.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)
