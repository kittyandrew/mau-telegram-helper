from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from modules.error_logging.error_catch_util import error_logger
from telethon import events
from PIL import Image
import urllib.request
import asyncio
import math
import io


async def init(bot):
    PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
    A pack can't have more than 120 stickers at the moment."
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$sticker"))
    @error_logger
    async def sticker_maker_handler(event):
        ''' Making packs of stickers, adding stickers to existing packs '''
        userbot = event.client
        user = await userbot.get_me()
        if not user.username:
            user.username = user.first_name
        message = await event.get_reply_message()
        photo = None
        emojibypass = False
        is_anim = False
        emoji = ""
        await event.edit("`Processing..`")
        if message and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = io.BytesIO()
                photo = await userbot.download_media(message.photo, photo)
            elif "image" in message.media.document.mime_type.split('/'):
                photo = io.BytesIO()
                await userbot.download_file(message.media.document, photo)
                if (DocumentAttributeFilename(file_name='sticker.webp') in message.media.document.attributes):
                    emoji = message.media.document.attributes[1].alt
                    emojibypass = True
            elif (DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in message.media.document.attributes):
                emoji = message.media.document.attributes[0].alt
                emojibypass = True
                is_anim = True
                photo = 1
            else:
                await event.edit("`Unsupported File!`")
                await asyncio.sleep(1)
                await event.delete()
                return
        else:
            await event.edit("`Command is not a reply!`")
            await asyncio.sleep(1)
            await event.delete()
            return

        try:
            if photo:
                cmnd_list = event.text.split()
                ''' Flags: 
                           -e or -emoji (followed by an emoji) : setting emoji to future sticker
                           -a (follow by a name) : appending to existing pack 
                           (if pack doesn't exist, new will be created)'''

                if not emojibypass:
                    emoji = "✨"
                pack = 1

                if len(cmnd_list) == 5:
                    command1 = cmnd_list[1]
                    command1_arg = cmnd_list[2]
                    command2 = cmnd_list[3]
                    command2_arg = cmnd_list[4]

                    if command1 == "-e" or command1 == "-emoji":
                        emoji = command1_arg
                    elif command1 == "-a":
                        name_ = f"{command1_arg}{pack}"

                    if command2 == "-e" or command2 == "-emoji":
                        emoji = command2_arg
                    elif command2 == "-a":
                        name_ = f"{command2_arg}"

                elif len(cmnd_list) == 3:
                    command1 = cmnd_list[1]
                    command1_arg = cmnd_list[2]
                    if command1 == "-e" or command1 == "-emoji":
                        emoji = command1_arg
                    elif command1 == "-a":
                        name_ = f"{command1_arg}"

                #packname = f"a{user.id}_by_{user.username}_{pack_to_name}"
                packname = f"a{user.id}_sticker_pack_{name_}"
                packnick = f"{name_} pack"
                cmd = '/newpack'
                file = io.BytesIO()

                if not is_anim:
                    image = await resize_photo(photo)
                    file.name = "sticker.png"
                    image.save(file, "PNG")
                else:
                    packname += "_anim"
                    packnick += " animated"
                    cmd = '/newanimated'

                response = urllib.request.urlopen(urllib.request.Request(f'http://t.me/addstickers/{packname}'))
                htmlstr = response.read().decode("utf8").split('\n')

            try:
                if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
                    async with userbot.conversation('Stickers') as conv:
                        await conv.send_message('/addsticker')
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packname)
                        x = await conv.get_response()
                        while x.text == PACK_FULL:
                            packname = f"a{user.id}_sticker_pack_{name_}"
                            packnick = f"{name_} pack"
                            name_ = f"{name_} {pack}"
                            pack += 1
                            await event.edit(f"`Pack is full! Creating new {packnick}.`")
                            await conv.send_message(packname)
                            x = await conv.get_response()
                            if x.text == "Invalid pack selected.":
                                await conv.send_message(cmd)
                                await conv.get_response()
                                # Ensure user doesn't get spamming notifications
                                await userbot.send_read_acknowledge(conv.chat_id)
                                await conv.send_message(packnick)
                                await conv.get_response()
                                # Ensure user doesn't get spamming notifications
                                await userbot.send_read_acknowledge(conv.chat_id)
                                if is_anim:
                                    await userbot.forward_messages('Stickers', [message.id], event.chat_id)
                                else:
                                    file.seek(0)
                                    await conv.send_file(file, force_document=True)
                                await conv.get_response()
                                await conv.send_message(emoji)
                                # Ensure user doesn't get spamming notifications
                                await userbot.send_read_acknowledge(conv.chat_id)
                                await conv.get_response()
                                await conv.send_message("/publish")
                                if is_anim:
                                    await conv.get_response()
                                    await conv.send_message(f"<{packnick}>")
                                # Ensure user doesn't get spamming notifications
                                await conv.get_response()
                                await userbot.send_read_acknowledge(conv.chat_id)
                                await conv.send_message("/skip")
                                # Ensure user doesn't get spamming notifications
                                await userbot.send_read_acknowledge(conv.chat_id)
                                await conv.get_response()
                                await conv.send_message(packname)
                                # Ensure user doesn't get spamming notifications
                                await userbot.send_read_acknowledge(conv.chat_id)
                                await conv.get_response()
                                # Ensure user doesn't get spamming notifications
                                await userbot.send_read_acknowledge(conv.chat_id)
                                await event.edit(f"Stickers: [{packnick}](t.me/addstickers/{packname})", parse_mode='md')
                                return
                        if is_anim:
                            await userbot.forward_messages('Stickers', [message.id], event.chat_id)
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message('/done')
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                else:
                    await event.edit("`Creating new pack..`")
                    async with userbot.conversation('Stickers') as conv:
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await userbot.forward_messages('Stickers', [message.id], args.chat_id)
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await userbot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await userbot.send_read_acknowledge(conv.chat_id)

                await event.edit(f"Stickers: [{packnick}](t.me/addstickers/{packname})", parse_mode='md')

            except Exception as e:
                print(e)
                await event.edit("`Error in stickers creation..`")
                await asyncio.sleep(1)
                await event.delete()
                return

        except Exception as e:
            print(e)
            await event.edit("`Error in formatting for stickers..`")
            await asyncio.sleep(1)
            await event.delete()
            return



    async def resize_photo(photo):
        ''' Resize the given photo to 512x512 '''
        image = Image.open(photo)
        maxsize = (512, 512)
        if (image.width and image.height) < 512:
            size1 = image.width
            size2 = image.height
            if image.width > image.height:
                scale = 512 / size1
                size1new = 512
                size2new = size2 * scale
            else:
                scale = 512 / size2
                size1new = size1 * scale
                size2new = 512
            size1new = math.floor(size1new)
            size2new = math.floor(size2new)
            sizenew = (size1new, size2new)
            image = image.resize(sizenew)
        else:
            image.thumbnail(maxsize)

        return image