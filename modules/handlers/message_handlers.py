from modules.utils.internet_apis import MyBingTranslator, GoogleAPI, YouTubeAPI, InstagramAPI
from modules.error_logging.error_catch_util import error_logger
from telethon.errors.rpcerrorlist import MessageIdInvalidError
from modules.utils.rextester_api import RexTesterAPI
from telethon import events
import asyncio
import re


async def init(bot):
    @bot.on(events.NewMessage(pattern=lambda text: text.startswith("$"), outgoing=True))
    @error_logger
    async def commands_applier(event):
        client = event.client
        try:
            text = event.text
            message = event.message
            user_id = event.from_id
            chat_id = event.to_id
        except Exception as e:
            print("commands applier tier 1 error.")
            print(e)


        try:
            Not = False
            try:
                replied_to = await event.get_reply_message()
                replied_to_id = replied_to.from_id
            except:
                Not = True

            # Commands which don't care if message is a reply or not
            # TODO: -m for custom name, different from search
            try:
                if text.startswith('$vid'):
                    try:
                        command1 = text.split()[1]
                    except:
                        command1 = None
                    try:
                        command2 = text.split()[2]
                    except:
                        command2 = None

                    commands = [command1, command2]

                    if ("-h" in commands) and ("-n" in commands):
                        search_text = " ".join(list(text.split()[3:]))
                        x = YouTubeAPI.searh_into_hyperlink(search_text, name_auto_correct=True)
                        await event.edit(x, parse_mode="HTML", link_preview=False)
                    elif "-h" in commands:
                        search_text = " ".join(list(text.split()[2:]))
                        x = YouTubeAPI.searh_into_hyperlink(search_text)
                        await event.edit(x, parse_mode="HTML", link_preview=False)
                    elif "-n" in commands:
                        search_text = " ".join(list(text.split()[2:]))
                        x = YouTubeAPI.searh_into_hyperlink(search_text, name_auto_correct=True)
                        await event.edit(x, parse_mode="HTML", link_preview=True)
                    else:
                        search_text = " ".join(list(text.split()[1:]))
                        x = YouTubeAPI.searh_into_hyperlink(search_text)
                        await event.edit(x, parse_mode="HTML", link_preview=True)

                elif text.startswith("$inst"):

                    try:
                        command1 = text.split()[1]
                    except:
                        command1 = None

                    if command1 == '-h':
                        search_name = " ".join(list(text.split()[2:]))
                        x = InstagramAPI.search_profile_into_hyperlink(search_name)
                        if 'no such profile' == x[0]:
                            await event.edit("No such profile..")
                            await asyncio.sleep(2)
                            await event.delete()
                        elif x[0]:
                            await event.edit(x[1], parse_mode="HTML", link_preview=False)
                        else:
                            raise Exception("Fail.")

                    else:
                        search_name = " ".join(list(text.split()[1:]))
                        x = InstagramAPI.search_profile_into_hyperlink(search_name)
                        if 'no such profile' == x[0]:
                            await event.edit("No such profile..")
                            await asyncio.sleep(2)
                            await event.delete()
                        elif x[0]:
                            await event.edit(x[1], parse_mode="HTML", link_preview=True)
                        else:
                            raise Exception("Fail.")

                elif text.lower() == "$f":

                    try:
                        await event.delete()
                        await client.send_file(chat_id, file="CAADAgADsAADTptkAler0GVnHyzGAg", reply_to=replied_to_id)
                    except Exception as e:
                        print(e)
                        try:
                            try:
                                await event.delete()
                            except:
                                pass
                            await client.send_file(chat_id, file="CAADAgADsAADTptkAler0GVnHyzGAg")
                        except Exception as e:
                            print(e)

                else:
                    pass#await event.delete()


            except Exception as e:
                print(e)
                await event.edit("Error.")
                await asyncio.sleep(3)
                await event.delete()
                raise e

            # Only commands for non-reply messages
            if Not:
                pass
            # Only reply's commnads
            else:  # TODO:TRANSLATE to language

                if text.startswith("$tr"):

                    try:
                        try:
                            lang = text.split()[1]
                        except:
                            lang = 'en'

                        text_tr = replied_to.text
                        trans = MyBingTranslator.translate(text_tr, lang=lang, tell_input_lang=True)
                        await event.edit(trans)

                    except Exception as e:
                        print("commands applier tier 2 error.")
                        print(e)

                elif text.startswith('$gtr'):

                        try:
                            lang = text.split()[1]
                        except:
                            lang = 'en'

                        text_tr = replied_to.text
                        trans = GoogleAPI.google_translate(text_tr, target=lang)
                        await event.edit(trans)

                elif text.startswith('$del'):
                    try:
                        try:
                            await replied_to.delete()
                        except Exception as e:
                            print(e)
                        try:
                            await event.delete()
                        except Exception as e:
                            print(e)
                    except:
                        pass

        except Exception as e:
            await event.edit("Error.")
            await asyncio.sleep(1)
            await event.delete()
            print(e)
            raise e

