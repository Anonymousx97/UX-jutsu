### Made by Ryuk ###
### based on code from ux ###

import os
import random
from nekosbest import Client, Result, models
from pyrogram.errors import MediaEmpty, WebpageCurlFailed
from wget import download
from userge import Message, userge


client = Client()

Tags = [tag for tag in (models.CATEGORIES)]

@userge.on_cmd(
    "bnekos",
    about={
        "header": "Get SFW stuff from nekos.best",
        "usage": "{tr}bnekos for random\n{tr}bnekos [Choice]",
        "Choice": Tags,
    },
)
async def neko_life(message: Message):
    choice = message.input_str
    if not choice:
            link = (await client.get_image(random.choice(Tags), 1)).url
    if choice:
        input_choice = (choice.strip()).lower()
        if input_choice in Tags:
            link = (await client.get_image(input_choice, 1)).url
        else:
            await message.err(
                "Choose a valid Input !, See Help for more info.", del_in=5
            )
            return
    await message.delete()

    try:
        await send_nekosbest(message, link)
    except (MediaEmpty, WebpageCurlFailed):
        link = download(link)
        await send_nekosbest(message, link)
        os.remove(link)


async def send_nekosbest(message: Message, link: str):
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if link.endswith(".gif"):
        #  Bots can't use "unsave=True"
        bool_unsave = not message.client.is_bot
        await message.client.send_animation(
            chat_id=message.chat.id,
            animation=link,
            unsave=bool_unsave,
            reply_to_message_id=reply_id,
        )
    else:
        await message.client.send_photo(
            chat_id=message.chat.id, photo=link, reply_to_message_id=reply_id
        )
