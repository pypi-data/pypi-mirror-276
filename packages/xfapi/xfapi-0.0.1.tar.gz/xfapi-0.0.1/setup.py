import setuptools
import re
import requests
from bs4 import BeautifulSoup
 
package_name = "xfapi"
 
 
def curr_version():
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    latest_version = soup.select_one(".release__version").text.strip()
    return str(latest_version)
 
 
def get_version():
   return "0.0.1"
 
 
def upload():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    with open('requirements.txt') as f:
        required = f.read().splitlines()
 
    setuptools.setup(
        name=package_name,
        version=get_version(),
        author="Alex_M",  # 作者名称
        author_email="asiaier@163.com", # 作者邮箱
        description="Apis tool base fastapi", # 库描述
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/xfapi/", # 库的官方地址
        packages=setuptools.find_packages(),
        data_files=["requirements.txt"], 
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=required,
    )
 
 
def write_now_version():
    print("Current VERSION:", get_version())
    with open("VERSION", "w") as version_f:
        version_f.write(get_version())
 
 
def main():
    try:
        upload()
        print("Upload success , Current VERSION:", "0.0.1")
    except Exception as e:
        raise Exception("Upload package error", e)
 
 
if __name__ == '__main__':
    main()