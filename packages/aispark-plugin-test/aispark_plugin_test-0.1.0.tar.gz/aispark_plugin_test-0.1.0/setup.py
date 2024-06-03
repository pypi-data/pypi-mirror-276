from setuptools import setup, find_packages

setup(
    name='aispark_plugin_test',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aispark-plugin-test=aispark_cli_plugin_assastant2_test20240602.shell.usage:run',
        ],
    },
    setup_requires=[
        # 列出setup需要的依赖项
    ],
    install_requires=[
        # 列出安装需要的依赖项
    ],
)
