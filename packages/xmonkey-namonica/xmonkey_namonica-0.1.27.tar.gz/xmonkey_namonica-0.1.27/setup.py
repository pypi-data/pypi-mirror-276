from setuptools import setup, find_packages

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xmonkey_namonica',
    version='0.1.27',
    description="Purl2Notices - OSS Attribution Generator",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author="Oscar Valenzuela",
    author_email="oscar.valenzuela.b@gmail.com",
    url='https://github.com/Xpertians/xmonkey-namonica',
    license='Apache 2.0',
    entry_points={
        'console_scripts': [
            'xmonkey-namonica = xmonkey_namonica.cli:main'
        ]
    },
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'xmonkey_namonica': ['datasets/*.pkl'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "spacy",
        "nltk",
        "scikit-learn==1.4.2",
        "pandas",
        "numpy",
        "requests",
        "urllib3",
        "python-magic",
        "beautifulsoup4",
        "oslili",
        "tqdm",
    ],
)
