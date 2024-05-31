from setuptools import setup, find_packages

setup(
    name='aura_tools',  # 包名
    version='0.22',  # 版本号
    packages=find_packages(),  # 自动找到包目录
    install_requires=[  # 依赖包
        # 'some_package>=1.0',
    ],
    entry_points={  # 可选的命令行工具
        'console_scripts': [
            'my_command=my_project.some_module:main',
        ],
    },
    author='aura_tools',
    author_email='aura_tools@topsmartdata.com',
    description='工具库',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aura-tools/aura_tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
