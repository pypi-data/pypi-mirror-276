# coding utf8
import setuptools
from yxmap.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="yxmap",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="Xu Yuxing's personal geographic data-processing tools",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/SouthernCD/yxmap",
    include_package_data = True,

    # entry_points={
    #     "console_scripts": ["HugeP2G = hugep2g.cli:main"]
    # },    

    packages=setuptools.find_packages(),

    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "geopandas>=0.14.3",
        "statsmodels>=0.14.1",
        "rasterio>=1.3.10",
    ],

    python_requires='>=3.5',
)