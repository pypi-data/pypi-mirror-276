from setuptools import setup, find_packages

setup(
    name='IDswapper',
    version='0.1.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'IDswapper=idswapper.fetchids:fetch_ids'
        ]
    },
    install_requires=[
        'pandas',
        'mysql-connector-python',
        'tqdm',
        'pymysql',
    ],
    package_data={'idswapper': ['fetchids.py', 'db_config.json', 'data_file.gz']},
    include_package_data=True,
    author='Pr (France) Dr. rer. nat. Vijay K. ULAGANATHAN',
    author_email='',
    description='A tool for swapping IDs in a file by fetching various IDs from idswapper database',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vkulaganathan/IDswapper/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

