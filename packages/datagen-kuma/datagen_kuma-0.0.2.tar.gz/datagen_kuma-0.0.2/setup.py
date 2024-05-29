import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datagen_kuma",
    version="0.0.2",
    author="devinu",
    author_email="iwlee.dev@gmail.com",
    description="DataGen is a library for generating test data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/develinu/datagen.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'asttokens==2.4.1',
        'colorama==0.4.6',
        'executing==2.0.1',
        'icecream==2.1.3',
        'numpy==1.26.4',
        'pandas==2.2.2',
        'Pygments==2.18.0',
        'python-dateutil==2.9.0.post0',
        'pytz==2024.1',
        'scipy==1.13.1',
        'six==1.16.0',
        'tzdata==2024.1',
        'uv==0.2.4',
    ],
    keywords='data generator datagen_kuma pandas dataframe fake',
    project_urls={
        'Homepage': 'https://github.com/develinu/datagen.git',
    },
)