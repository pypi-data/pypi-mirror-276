from setuptools import setup, find_packages

setup(
    name="Text-to-Image-Generator",
    version="0.0.1",
    description="A project that combines a FastApi backend with an ML service to generate images from text.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Anna Fomina Melnikova Maria",
    author_email="anna.skachenko@gmail.com",
    url="https://github.com/AnnaFomina1997/Text-to-Image-Generator.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "jinja2",
        "requests",
        "diffusers",
        "torch",
        "GPUtil",
        "numba",
    ],
    entry_points={
        "console_scripts": [
            "backend = backend.app.main:app",
            "ml_service = ml_service.app.main:app"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
