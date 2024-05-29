import setuptools
import chardet

# Detect encoding for README.md
with open("README.md", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

with open("README.md", "r", encoding=encoding) as fh:
    long_description = fh.read()

# Detect encoding for requirements.txt
with open("requirements.txt", "rb") as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

with open("requirements.txt", "r", encoding=encoding) as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="contacts_assistant",
    version="0.0.14",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    include_package_data=True,
    author="Mykyta Samoilenko",
    author_email="inikita546@gmail.com",
    description="Contacts Assistant is a bot designed to help you manage your address book efficiently. Below is a list of available commands, their functions, and required arguments. Additionally, you can add your notes to our notebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bignichok/Python-ContactsAssistant",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'contacts_assistant=main:main'
        ]
    },
)
