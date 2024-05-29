from setuptools import find_packages, setup

setup(
    name="nonebot_plugin_setu4",
    version="0.15.114514.2",
    author="Special-Week",
    author_email="HuaMing27499@gmail.com",
    description="内置数据库的setu插件, 尝试降低因为风控发不出图的概率",
    python_requires=">=3.9.0",
    packages=find_packages(),
    url="https://github.com/Special-Week/nonebot_plugin_setu4",
    package_data={"nonebot_plugin_setu4": ["resource/*"]},
    install_requires=["pillow>=9.1.1", "nonebot2", "nonebot-adapter-onebot", "httpx"],
)
