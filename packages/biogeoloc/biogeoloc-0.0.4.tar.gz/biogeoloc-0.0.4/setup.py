# coding utf8
import setuptools
from biogeoloc.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="biogeoloc",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="A python object package for storing and managing geographic information about biological samples.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/SouthernCD/biogeoloc",
    include_package_data = True,

    # entry_points={
    #     "console_scripts": ["HugeP2G = hugep2g.cli:main"]
    # },    

    packages=setuptools.find_packages(),

    install_requires=[
        "yxmath",
        "yxmap",
        "yxutil",
        "pandas",
        "numpy",
    ],

    python_requires='>=3.5',
)