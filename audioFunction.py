import discord
from gtts import gTTS
from datetime import datetime
from typing import Tuple, List, Dict


def text_to_speech(message: str) -> Tuple[discord.File, str]:

    """
    Get the file handle for speech from text

    :param message: input message to be turned into audio file
    :return: object for discord bot sending, and file path
    """

    now = datetime.now().strftime("%Y%m%d %H%M%S%f")
    #print("date and time:", now)

    mp3 = gTTS(text=message, lang="en", slow=False)
    # await message.channel.send(mp3)
    mp3.save(path := f"{now}.mp3")

    file = discord.File(path)
    return file, path
