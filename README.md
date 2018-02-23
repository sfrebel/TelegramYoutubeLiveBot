# TelegramYoutubeLiveBot
This is a Project for a Telegram bot which notifies you if a Youtube Chanel starts a new Livestream.

## Setup
For the bot to work you need to do a few things

### Install python
I tested the bot using Python 3.6.4, so you may want to install that :P You also need to install two librarys.
```
pip install python-telegram-bot --upgrade
pip install requests --upgrade
```
### Configure the Bot
For the Bot to run you need to change at least three things in the [config.json](https://github.com/sfrebel/TelegramYoutubeLiveBot/blob/master/config.json).

1. You need to create a Bot in Telegram and provide the Token you receive from the BotFather. Here is [a good guide](https://core.telegram.org/bots#6-botfather) how you do that exactly.
2. You need a API key to use the Youtube API v3. [Here is how.](https://developers.google.com/youtube/registering_an_application)
3. You need to obtain the ID of the Youtubechanel you want to get notified. It is part of the URL of the chanel. https://www.youtube.com/channel/UCtI0Hodo5o5dUb67FeUjDeA is the url of the SpaceX chanel and the ChanelId is `UCtI0Hodo5o5dUb67FeUjDeA` so it should be easy for you to determine the ID for the chanel you want.
4. You may want to change the frequency the Bot checks for new streams. Keep in mind that the Youtube API has [a Quota limit of one million units per day](https://developers.google.com/youtube/v3/getting-started#quota) So dont set the frequencie to high if you want to use the bot in multiple Chats. One get request cost 170 units in my testing.

### Run the Bot

After all that you can simply run the bot by executing [TelegramYoutubeLiveBot.py](https://github.com/sfrebel/TelegramYoutubeLiveBot/blob/master/TelegramYoutubeLiveBot.py). You may want to use something like [Screen](https://wiki.ubuntuusers.de/Screen/) to keep the bot running in the background.

Then simply start the bot by sending the message `/start`. This also works in Group chats (the bot needs to be a member of the Group)

## Planed Features
* Setting the interval using commands
* Setting the youtubechanel using commands (and maybe use the Chanelname instead of the ID)
* Make it possible to follow more than one chanel
* Restrict command use to specific people in Groupchats (e.g. Admins)
