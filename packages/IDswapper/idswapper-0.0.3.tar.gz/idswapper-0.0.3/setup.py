from setuptools import setup, find_packages

setup(
    name='IDswapper',
    version='0.0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'IDswapper=idswapper.fetchids:main'
        ]
    },
    install_requires=[
        'tqdm',
        'pymysql',
    ],
    package_data={'idswapper': ['db_config.json']},
    include_package_data=True,
    author='Pr (France) Dr. rer. nat. Vijay K. ULAGANATHAN',
    author_email=' ',
    description='A tool for swapping IDs in a file and fetching data from a MySQL database',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vkulaganathan/IDswapper/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

