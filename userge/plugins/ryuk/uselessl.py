from userge import Message, userge
from pyrogram.errors import MediaEmpty, WebpageCurlFailed

@userge.on_cmd("leech",about={"flags":"-p for pic\n-v for vid\n-d for doc"})
async def leech(message:Message):
    rw_inp = message.filtered_input_str
    try:
        if "-p" in message.flags:
            await message.reply_photo(rw_inp)
        elif "-v" in message.flags:
            await message.reply_video(rw_inp)
        elif "-d" in message.flags:
            await message.reply_document(rw_inp)
        else:
            await message.edit("Flag not provided.\nProcess Aborted.")
    except (MediaEmpty, WebpageCurlFailed):
        await message.edit("Instant leech failed due to webpage can't be curled by TG.")
