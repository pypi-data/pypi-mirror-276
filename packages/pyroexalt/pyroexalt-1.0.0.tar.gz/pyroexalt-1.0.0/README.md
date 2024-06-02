<p align="center">
    <a href="https://github.com/Mayuri-Chan/pyrofok">
        <img src="https://docs.pyrogram.org/_static/pyrogram.png" alt="Pyrofork" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://github.com/Mayuri-Chan">
        Homepage
    </a>
    •
    <a href="https://github.com/Mayuri-Chan/pyrofork/issues">
        Issues
    </a>
    •
    <a href="https://t.me/FZXParadox">
        Support Channel
    </a>
</p>

## PyroExalt 

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots
> Made for Private Use, Not for Production, No Copyright Intentioned 

``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrofork!")


app.run()
```
