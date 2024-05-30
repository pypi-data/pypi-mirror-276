from setuptools import setup, find_packages

setup(
    name="fast_auth_routes",
    version="0.1.0",
    description="A simple FastAPI application with authentication and user management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ewerton Azevedo",
    author_email="ewertonzvd@gmail.com",
    url="https://github.com/seunome/myapp",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "passlib[bcrypt]",
        "python-jose[cryptography]",
        "motor"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)