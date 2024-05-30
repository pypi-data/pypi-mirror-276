from setuptools import setup, find_packages

setup(
    name="anon_traffic",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # 在这里列出你的依赖包，例如：
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "anon_traffic.disanon=anon_traffic.decrypt:decrypt",
        ],
    },
    author="aimafan",
    author_email="chongrufan@nuaa.edu.cn",
    description="disanon ip and port",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aimafan/anon_traffic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
