from setuptools import setup, find_packages

setup(
    name='pytest_zcc',
    url='https://github.com/xx/',
    version='1.4',
    author='zcc',
    author_email="1059995908@qq.com",
    description='eee',
    long_description='eee',
    classifiers=[
        # pipy搜索索引分类
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
    license='xxxxxx',
    packages=find_packages(),
    keywords=[
        'pytest', 'py.test', 'pytest_zcc'
    ],
    install_requires=[
        'pytest'
    ],
    entry_points={
        'pytest11':[
            'pytest_zcc = pytest_zcc.pytest_zccdev'
        ]
    },
    zip_safe=False
)