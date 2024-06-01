from setuptools import setup, find_packages

setup(
    name="cn-stock-holidays-pro",
    version="1.8",
    packages=find_packages(),
    install_requires=[
        'requests',
        'faker',
        'execjs',
        'loguru',
        'base64',
        'hashlib',
        'Crypto',
        'pandas',
        'fuzzywuzzy',
        'httpx',
        'Pillow',
        'playwright',
        'PyExecJS',
        'redis',
        'fastapi',
        'uvicorn',
        'APScheduler',
        'beautifulsoup4',
        'bs4',
        'certifi',
        'clickhouse-driver',
        'curl-cffi',
        'DrissionPage',
        'fake-useragent',
        'Flask',
        'Flask-APScheduler',
        'Flask-Cors',
        'frida',
        'gevent',
        'httpx',
        'Jinja2',
        'langchain',
        'langchain-community',
        'suiutils-py',
    ],

    # metadata for upload to PyPI
    author="yanjlee",
    author_email="yanjlee@163.com",
    description="A List of china stock exchange holidays",
    license="MIT",
    keywords="china stock holiday exchange shanghai, shenzhen and hongkong",
    url="https://github.com/yanjlee/cn_stock_holidays.git",  # project home page, if any

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
    },
    entry_points={
        'console_scripts': [
            'cn-stock-holiday-sync=cn_stock_holidays.data:sync_data',
            'cn-stock-holiday-sync-hk=cn_stock_holidays.data_hk:sync_data',
            'get-day-list=cn_stock_holidays.tools.cmd:main',
        ]
    }
)
