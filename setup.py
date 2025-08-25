from setuptools import setup, find_packages
import os


# 我們需要讓 patterns 資料夾也跟著一起打包
def find_pattern_files(directory):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".json"):
                # 我們需要的是相對於 'hacker_gf' 模組的路徑
                paths.append(os.path.join("..", path, filename))
    return paths


pattern_files = find_pattern_files("hacker_gf/patterns")


setup(
    name="hacker_gf",
    version="0.1.0",
    description="A Pure Python, grep-free, spiritual successor to gf, designed for structured output and easy integration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="begineer-py",  # 換成你的名字
    author_email="your-email@example.com",  # 可選
    url="https://github.com/begineer-py/hacker_gf",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "hacker_gf": ["patterns/*.json"],
    },
    entry_points={
        "console_scripts": [
            "hacker_gf = hacker_gf.pygf_engine:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.6",
)
