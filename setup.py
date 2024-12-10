from setuptools import setup, find_packages

setup(
    name="friday",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "fastapi==0.75.1",
        "sqlalchemy==1.4.35",
        "mysqlclient==2.1.0",
        "uvicorn[standard]==0.17.6",
        "python-dotenv==0.20.0",
        "strawberry-graphql[fastapi]>=0.205.0",
        "pytest>=7.4.3",
        "pytest-cov>=4.1.0",
        "pytest-asyncio>=0.21.1",
        "types-pytest>=7.4.0",
    ],
)
