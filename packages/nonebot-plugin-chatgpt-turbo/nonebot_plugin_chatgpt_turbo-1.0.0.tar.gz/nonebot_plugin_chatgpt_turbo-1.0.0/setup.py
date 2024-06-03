# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_chatgpt_turbo']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'openai>=1.30.5,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-chatgpt-turbo',
    'version': '1.0.0',
    'description': 'A nonebot plugin for oneapi and openai',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-chatgpt-turbo\n</div>\n\n# 介绍\n- 本插件适配OneAPI和OpenAI接口，可以在nonebot中调用OpenAI官方或是OneAPI(gpt系列模型,gemini-1.5-pro)接口的模型进行回复。\n- 本插件具有上下文回复和多模态识别（识图）功能。\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_chatgpt_turbo.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-gpt3.5-turbo"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-chatgpt-turbo\n  ```\n\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n```\noneapi_key = ""  # OpenAI官方或者是支持OneAPI的大模型中转服务商提供的KEY\noneapi_model = "gpt-4o" # 使用的语言大模型，使用识图功能请填写合适的大模型名称\n```\n\n可选内容：\n```\noneapi_url = ""  # （可选）大模型中转服务商提供的中转地址，使用OpenAI官方服务不需要填写\nenable_private_chat = True   # 私聊开关，默认开启，改为False关闭\n```\n\n# 效果\n![](demo.jpg)\n\n# 使用方法\n\n- @机器人发送问题时机器人不具有上下文回复的能力\n- chat 使用该命令进行问答时，机器人具有上下文回复的能力\n- clear 清除当前用户的聊天记录\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
