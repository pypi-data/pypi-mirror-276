# -*- coding: utf-8 -*-
r"""
Created on 2024/6/2 0:57
rd /S /Q "d:\pybuild"&&mkdir "d:\pybuild"&&pyinstaller D:/python/函数/pip\setup.py.py --workpath d:\pybuild  --distpath d:\pybuild\dist
"""
import setuptools


setuptools.setup(
    name="MzhFunc",
    version='0.0.1',
    author="Author's name",  # 作者名称
    author_email="xxxxxxx@163.com",  # 作者邮箱
    description="Python helper tools",  # 库描述
    long_description='python for mytools',
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/yourtools/",  # 库的官方地址
    packages=setuptools.find_packages(),
    data_files=["requirements.txt"],  # yourtools库依赖的其他库
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)


