from setuptools import setup, find_packages

setup(
    name='scrapedin',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'unidecode',
        'pandas',
        'datetime',
        'psutil',
        'cprofile',
        'os',
        'sys',
        'pickle',
        'csv',
        'time',
        'logging',
        'asyncio',
        'regex'
    ],
    author='Sambiote',
    description='A package for scraping job listings from LinkedIn',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
