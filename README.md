[![PyPI version](https://badge.fury.io/py/TwitterFollowBot.svg)](https://badge.fury.io/py/TwitterFollowBot)
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

# Telegram Bot

[![Join the chat at https://gitter.im/rhiever/TwitterFollowBot](https://badges.gitter.im/rhiever/TwitterFollowBot.svg)](https://gitter.im/rhiever/TwitterFollowBot?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python bot that automates several actions on Telegram, such as sending messages to group of users.

## Disclaimer

## Installation

You can install the Telegram Bot using `pip`:

    pip install TelegramBot

Dependencies

### Create an instance of the bot

To create an instance of the bot:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot()
    
    
By default, the bot will look for a configuration file called `config.txt` in your current directory.
    
If you want to use a different configuration file, pass the configuration file to the bot as follows:

    from TwitterFollowBot import TwitterBot
    
    my_bot = TwitterBot("my-other-bot-config.txt")
    
## Note for me

https://www.codementor.io/djangostars/create-deploy-telegram-bot-python-7jggn472x

## Have questions? Need help with the bot?

If you're having issues with or have questions about the bot, [file an issue](https://github.com/juno249/TeleBot/issues) in this repository so one of the project managers can get back to you. **Please [check the existing (and closed) issues](https://github.com/juno249/TeleBot/issues?utf8=%E2%9C%93&q=is%3Aissue) to make sure your issue hasn't already been addressed.**