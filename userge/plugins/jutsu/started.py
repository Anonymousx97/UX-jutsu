# plugin made for USERGE-X by @Kakashi_HTK(TG)/@ashwinstr(GH)
# before porting please ask to Kakashi

import asycnio
from userge import userge, Message, Config

CHANNEL = userge.getCLogger(__name__)

async def main():
    await CHANNEL.log("<b>BOT HAS STARTED SUCCESSFULLY.<b>")

if __name__ == "__main__":
    asyncio.run(main())