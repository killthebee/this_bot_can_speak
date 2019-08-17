# Speaking bot
With this bot you can practice Russian(to some extend) in VK or TG. Without being persuaded to drink vodka nor play CS:GO.

See it for yourself:





<p align="center">
  <img src="https://github.com/killthebee/this_bot_can_speak/blob/master/gifs/%D1%82%D0%B3%D0%B1%D0%BE%D1%82.gif"/>
</p>




<p align="center">
  <img src="https://github.com/killthebee/this_bot_can_speak/blob/master/gifs/%D0%B2%D0%BA%D0%B1%D0%BE%D1%82.gif"/>
</p>




### How to install

Python3 should be already installed.

Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```

pip install -r requirements.txt

```
Also, you need to create your DialogFlow project and one agent in it.

You can name agent all you want, but make sure to set ru language code.

Then you need to fetch your very own google application credentials json file. Go [here](https://cloud.google.com/docs/authentication/getting-started) for more information.

And make 2 Telegram bots, 1 vk community and gather their api tokens. 1 form VK, [info](https://vk.com/dev/bots_docs?f=1.1.%2B%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2B%D0%BA%D0%BB%D1%8E%D1%87%D0%B0%2B%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0). 2 from Telegram's [botFather](https://medium.com/shibinco/create-a-telegram-bot-using-botfather-and-get-the-api-token-900ba00e0f39).


### Launch example

Before begin make sure what you set up enviroment variables as listed below.
Run launcher.py with positional arg TG or VK, what way app will know witch bot to launch. In addition you can use optional arg -t Yes if you need to teach your bot some phrases. Like in example below.
```

python launcher.py TG -t Yes

```


### Enviroment Variables

GOOGLE_APPLICATION_CREDENTIALS here must be stored path to your google application credentials json file.

DIALOGFLOW_PROJECT_ID name of your dialog flow project.

TG1_TOKEN api token of your main telegram bot.

TG2_TOKEN api token of your auxilary telegram bot.

VK_TOKEN vk api token.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
