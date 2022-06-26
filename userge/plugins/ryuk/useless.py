from userge import Message, userge

CHANNEL = userge.getCLogger(__name__)


@userge.on_cmd(
    "jc",
    about={
        "header": "join private chat using link",
        "usage": "{tr}jc chatlink",
    },
)
async def jc(message: Message):
    reply = message.reply_to_message.text
    link = reply if reply else message.input_str
    if not link:
        await message.edit(
            "```Bruh, Without chat name, I can't Join...^_^```", del_in=3
        )
        return
    try:
        await userge.join_chat(link)
    except KeyError:
        await userge.join_chat(link.split("/")[-1])
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
    try:
        if button_name:
            await button.click(button_name)
        else:
            await button.click(0)
    except TimeoutError:
        return
