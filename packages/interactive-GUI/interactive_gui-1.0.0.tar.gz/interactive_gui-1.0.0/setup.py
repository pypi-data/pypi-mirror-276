from setuptools import setup, find_packages

setup(
    name='interactive_GUI',  # 包的名称
    version='1.0.0',    # 版本号
    packages=find_packages(),  # 包含的包列表，使用 find_packages() 可以自动发现所有包
    install_requires=[  # 项目依赖的第三方包列表
        'matplotlib',
        'numpy',
        'scipy',
        'vpython'
    ],

    author='LI XIANG XIAN FENG',  # 作者信息
    author_email='1111111111@qq.com',
    description='Description of my project',  # 项目描述
    long_description=open('README.md').read(),  # 长描述，通常从 README 文件中读取
    long_description_content_type='text/markdown',  # 长描述的内容类型
    # url='https://github.com/yourusername/my_project',  # 项目主页
    license='MIT',  # 许可证信息
    # classifiers=[  # 分类器列表，用于 PyPI 的分类
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: 3.9',
    # ],
)


