# Terminal-Bot

**see this bot alive:** __https://t.me/HerokuTerminal_Bot__

## With this bot you can execute system commands on your server.

### how to config?
___

- clone or fork this repo
- give me a star 😎
- edit the [config.py](https://github.com/moshe-coh/Terminal-Bot/blob/main/config.py) file like this:

```python3
token = ""  # from @BotFather
app_id = 6  # https://my.telegram.org/apps
app_hash = ""  # https://my.telegram.org/apps
allowed = [12345678, 87654321]  # replace to your id (get your id in @userinfobot)

logger: bool = True  # set it True to get logs in some channel...
log_channel = -100

# if logger is True your channel ID and add it here.
# (don't forget to add your bot as admin in your channel...)

```
- run ```pip3 install -r requirements.txt```
- **and than run it on your sever!**

## how to deploy 
___

- [**see this video to deploy on VPS**](https://drive.google.com/file/d/1pbeg3eeim1F2XPFct-UTi9I9hHqYdH0-)

- [**see this video to deploy on _heroku_**](https://drive.google.com/file/d/1bchJpwyOMRgr5kI4CTuwW9RoCAv3Y5ho/view?usp=sharing)

## commnads for @BotFather:
```
start - 📜 welcome message 
help - 😉 like start message
ip - 🔒 my server ip
st - ♨️ speed test to my server 
stats - 📊 server stats
```

![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=moshe-coh&repo=Terminal-Bot)

## Todo
- [ ]  Add option to download and upload files...
- [ ]  Add /cd command
- [ ]  Add more commands...
