from modules.utils.functions import find_commands
from telethon import events
import config as c
import re


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$todo([\s\S]*)"))
    async def todo_manager(event):
        client = event.client
        commands, query = find_commands(event.pattern_match.group(1))
        try:
            await event.edit("Managing..")
        except:
            pass

        if "-get" in commands:
            if "-reverse" in commands or "-r" in commands:
                reverse = True
            else:
                reverse = False

            have_num = False
            for i in range(1, 11):
                if f"-{i}" in commands:
                    num = i
                    have_num = True
                    break
            if not have_num:
                num = 10


            msgs = client.iter_messages(c, reverse=reverse)
            pattern = re.compile(r"#TODO:.*")
            messages_ = list()
            ii = 1
            async for msg in msgs:
                if len(messages_) < 10:
                    if msg.text != None:
                        if re.findall(pattern, msg.text):
                            messages_.append((ii,msg))
                            ii += 1
                else:
                    break

            new_text = ""
            for each in messages_:
                tmp_text = each[1].text[:each[1].text.index("#TODO:")]
                tmp_id = each[1].text[each[1].text.index("#TODO:") + 6:]
                tmp_text = tmp_text.strip().strip("\n").strip()
                new_text += f"**{each[0]}.** {tmp_text} (ID:{tmp_id})\n"
            await event.edit(new_text)

        else:
            msgs = client.iter_messages(c)
            pattern = re.compile(r"#TODO:.*")
            list_of_ids = []
            async for msg in msgs:
                if msg.text != None:
                    num = int(re.search(pattern, msg.text).group(0).strip("#TODO:"))
                    if num not in list_of_ids:
                        list_of_ids.append(num)
            list_of_ids = sorted(list_of_ids)
            if len(list_of_ids) == 0:
                n = 1
            else:
                for n in range(1, 10000):
                    if n not in list_of_ids:
                        break
            new_todo = f"{query}\n#TODO:{n}"
            await client.send_message(c, new_todo)
            await event.edit(f"Ready! Task\n`{query}`\nwas added.")