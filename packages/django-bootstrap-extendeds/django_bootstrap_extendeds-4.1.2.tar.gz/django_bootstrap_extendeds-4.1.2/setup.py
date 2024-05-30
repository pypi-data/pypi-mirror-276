from setuptools import setup, find_packages

setup(
    name="django_bootstrap_extendeds",
    version="4.1.2",
    author="Dex",
    author_email="censored@gmail.com",
    description="Flask bootstrap-library EXTENDED",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/my_library",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['demo/**/*', 'main/**/*', '*.sqlite3', '.gitignore'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
