# coding utf8
import setuptools
from yxsql.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="yxsql",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="Xu Yuxing's personal sqlite orm.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/SouthernCD/yxsql",
    include_package_data = True,

    # entry_points={
    #     "console_scripts": ["HugeP2G = hugep2g.cli:main"]
    # },    

    packages=setuptools.find_packages(),

    install_requires=[
        "yxutil",
    ],

    python_requires='>=3.5',
)