from userge import Message, userge
from pyrogram.errors import UsernameInvalid


@userge.on_cmd(
    "jc",
    about={
        "header": "join private / public chat using link",
        "usage": "{tr}jc chatlink",
    },
)
async def jc(message: Message):
    reply = message.reply_to_message
    link = message.input_str or reply.text
    if not link:
        await message.edit(
            "Bruh, Without chat link, I can't Join...^_^", del_in=3
        )
        return
    try:
        await userge.join_chat(link)
    except UsernameInvalid:
        link = link.split("/")[-1]
        await userge.join_chat(link)
    except Exception as e:
        if str(e).startswith("Telegram says: [400 Bad Request] - [400 INVITE_REQUEST_SENT]"):
            return await message.reply("Join Request Sent.")
    return await message.reply("Joined")



@userge.on_cmd(
    "click",
    about={
        "header": "click buttons",
        "header": "Input which button you want to press\ndefaults to 1st button",
        "usage": "{tr}click yes",
    },
)
async def clck(message: Message):
    button_name = message.input_str
    button = message.reply_to_message
    if not button:
        return await message.edit("Reply to a button -_-", del_in=5)
    try:
        if button_name:
            await button.click(button_name)
        else:
            await button.click(0)
    except ValueError:
        return await message.reply("Button doesn't exists")
    except TimeoutError:
        return
