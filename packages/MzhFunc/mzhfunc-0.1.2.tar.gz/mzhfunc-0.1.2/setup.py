# -*- coding: utf-8 -*-
r"""
Created on 2024/6/2 0:57
rd /S /Q "d:\pybuild"&&mkdir "d:\pybuild"&&pyinstaller D:/python/函数/MzhFunc\setup.py.py --workpath d:\pybuild  --distpath d:\pybuild\dist

cd MzhFunc & del /q dist && del /q MzhFunc.egg-info && python setup.py sdist && twine upload dist/*

"""
import os
import re
import requests
import setuptools
from bs4 import BeautifulSoup


def curr_version():
    # 方法2：从官网获取版本号
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    latest_version = soup.select_one(".release__version").text.strip()
    return str(latest_version)


def get_version():
    # 从版本号字符串中提取三个数字并将它们转换为整数类型
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", curr_version())
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))
    # 对三个数字进行加一操作
    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    new_version_str = f"{major}.{minor}.{patch}"
    return new_version_str


ls = os.listdir('db')
ls.remove('__init__.py')
package_name = ls[0].split('.')[0]
setuptools.setup(
    name=package_name,
    version=get_version(),
    author="Author's name",  # 作者名称
    author_email="191891173@qq.com",  # 作者邮箱
    description="Python helper tools",  # 库描述
    long_description='python for mytools',
    long_description_content_type="text/markdown",
    url=f"https://pypi.org/project/{package_name}/",  # 库的官方地址
    packages=setuptools.find_packages(),
    # data_files=["requirements.txt"],  # yourtools库依赖的其他库
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
