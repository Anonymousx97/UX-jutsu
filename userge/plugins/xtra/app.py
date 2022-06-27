"""Fetch App Details from Playstore.
.app <app_name> to fetch app details.
By - @kirito6969
"""

import bs4
import aiohttp

from userge import Message, userge


@userge.on_cmd(
    "app",
    about={
        "header": "Search application details of any app\n"
        "in play store.\n"
        "Plugin by - @kirito6969,@krishna_singhal"
    },
)
async def app(message: Message):
    try:
        await message.edit("`Searching...`")
        app_name = "+".join(message.input_str.split(" "))
        async with aiohttp.ClientSession() as ses, ses.get(
            f"https://play.google.com/store/search?q={app_name}&c=apps"
        ) as res:
            result = bs4.BeautifulSoup(
                await res.text(),
                "lxml",
                parse_only=bs4.SoupStrainer("div", class_="ipRz4"),
            )

        app_name = result.find("div", class_="vWM94c").text
        app_dev = result.find("div", class_="LbQbAe").text
        app_dev_link = (
            "https://play.google.com/store/apps/developer?id="
            + app_dev.replace(" ", "+")
        )
        app_rating = (
            result.find("div", class_="TT9eCd")["aria-label"]
            .replace("Rated ", "⭐️ ")
            .replace(" out of ", "/")
            .replace(" stars", "", 1)
            .replace(" stars", "⭐️")
            .replace("five", "5")
        )
        app_link = "https://play.google.com" + result.find("a", class_="Qfxief")["href"]
        app_icon = result.find("img", class_="T75of bzqKMd")["src"]

        app_details = f"[📲]({app_icon}) **{app_name}**\n\n"
        app_details += f"`Developer :` [{app_dev}]({app_dev_link})\n"
        app_details += f"`Rating :` {app_rating}\n"
        app_details += f"`Features :` [View in Play Store]({app_link})"
        await message.edit(app_details, disable_web_page_preview=False)
    except IndexError:
        await message.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await message.err(err)
