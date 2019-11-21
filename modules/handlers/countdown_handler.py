from modules.error_logging.error_catch_util import error_logger
from modules.countdown_solvers import AsyncNumberGame, TextGame
from modules.utils.functions import async_find_commands
from telethon import events


async def init(bot):
    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$cdnum (\d+.?\d*?) ((\d+\,?)+)"))
    @error_logger
    async def countdown_numbers(event):
        commands, _useless = await async_find_commands(event)

        goal:str = event.pattern_match.group(1)
        if goal.isdecimal():
            goal = float(goal)
        else:
            goal = int(goal)
        numbers:str = event.pattern_match.group(2)
        numbers = numbers.split(",")

        # Init game number class
        game = AsyncNumberGame(numbers, goal)

        # Check for all results
        await event.edit("Doing some extraordinary calculations..")
        if "-all" in commands:
            solutions = await game.get_all()
            texted = '\n   '.join([f'{x}={y}' for x,y in solutions])
            await event.edit(f"```Solutions:\n   {texted}```")
        else:
            solution = await game.get_any()
            await event.edit(f"```Solution:\n   {solution[0]}={solution[1]}```")

    @bot.on(events.NewMessage(outgoing=True, pattern=r"^\$cdword ((\w+\,?)+)"))
    @error_logger
    async def countdown_words(event):
        commands, _useless = await async_find_commands(event)

        symbols:str = event.pattern_match.group(1)
        symbols = symbols.split(",")

        # Init game text class
        game = TextGame(symbols)

        # Check for all results
        await event.edit("Looking up the dictionary..")
        if "-all" in commands:
            solutions = game.get_all()
            texted = '\n   '.join(solutions)
            await event.edit(f"```Words:\n   {texted}```")
        else:
            solution = game.get_best()
            await event.edit(f"```Word:\n   {solution}```")

