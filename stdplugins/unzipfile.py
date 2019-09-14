""" command: .compress """

import asyncio
import os
import time
import zipfile

from telethon import events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter
import time
from datetime import datetime
from pySmartDL import SmartDL
from zipfile import ZipFile

extracted = Config.TMP_DOWNLOAD_DIRECTORY + "/extracted/"
thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"

@borg.on(admin_cmd(pattern=("unzip")))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))

        unzip = zipfile.ZipFile(downloaded_file_name,'r')
        unzip.extractall()
        for x in range(len(zipfile.namelist(downloaded_file_name))):
            await borg.send_file(
                            event.chat_id,
                            extracted,
                            caption="unzipped",
                            force_document=True,
                            allow_cache=False,
                            reply_to=event.message.id,
                            # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            #     progress(d, t, event, c_time, "trying to upload")
                            # )
                        )

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)