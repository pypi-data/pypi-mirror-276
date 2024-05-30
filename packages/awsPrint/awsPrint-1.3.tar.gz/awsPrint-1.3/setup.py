from setuptools import setup, find_packages

setup(
    name='awsPrint',  # 包名
    version='1.3',  # 版本
    description="colorful print",  # 包简介
    # long_description=open('README.md', 'r', encoding='utf-8').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='Gorkor',  # 作者
    author_email='2226750760@qq.com',  # 作者邮件
    maintainer='Gorkor',  # 维护者
    maintainer_email='2226750760@qq.com',  # 维护者邮件
    license='MIT License',  # 协议
    url='https://github.com/Gorkor227/awsPrint',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3',  # 设置python版本要求
    install_requires=['typing_extensions'],  # 安装所需要的库
    # entry_points={
    #     'console_scripts': [
    #         ''],
    # },  # 设置命令行工具(可不使用就可以注释掉)

)

