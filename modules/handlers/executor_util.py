from modules.error_logging.error_catch_util import error_logger
from modules.utils.async_executor_util import KExec
from telethon import events
from os import remove
import asyncio


async def init(bot):
    @bot.on(events.MessageEdited(outgoing=True, pattern=r"^\$exec([\s\S]*)"))
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$exec([\s\S]*)"))
    @error_logger
    async def execute_code(run_q):
        if not run_q.text[0].isalpha() and run_q.text[0] not in ("/", "#", "@", "!"):
            try:
                replied_to = await run_q.get_reply_message()
            except:
                replied_to = None

            if replied_to is None:
                try:
                    code = run_q.pattern_match.group(1)
                    code = code.strip("\n")
                except:
                    print("didnt work")
            else:
                if len(run_q.text.split()) > 1:
                    code = run_q.pattern_match.group(1)
                    code = code.strip("\n")
                else:
                    code = replied_to.text

            if run_q.is_channel and not run_q.is_group:
                await run_q.edit("`Exec isn't permitted on channels!`")
                await asyncio.sleep(2)
                await run_q.delete()
                return

            if not code:
                await run_q.edit("``` There are no code to be executed..```")
                await asyncio.sleep(2)
                await run_q.delete()
                return

            if code in ("telethon sessions/My personal account keeper.session", "config.env"):
                await run_q.edit("`That's a dangerous operation! Not Permitted!`")
                await asyncio.sleep(2)
                await run_q.delete()
                return

            try:
                await run_q.edit("Executing..")
            except:
                pass
            block_of_code = "".join(f"\n{l.strip()}" for l in code.split("\n.strip()"))

            result = str(await KExec(block_of_code).eval(c=run_q.client, e=run_q))

            # Handle too long output (writing it to *.txt file and sending)
            if len(result) > 1024:
                file_name = "buffer/output.html"
                file = open(file_name, "w+")
                file.write(result)
                file.close()
                await run_q.client.send_file(
                        run_q.chat_id,
                        file_name,
                        reply_to=run_q.id,
                        caption="`Open to see result of the operation`",
                    )
                remove("output.txt")
                return
            else:
                await run_q.edit(result)
