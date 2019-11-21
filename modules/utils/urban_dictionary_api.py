import aiohttp
import asyncio
import html


class UrbanDicAPI:

    RANDOM_URL = 'https://api.urbandictionary.com/v0/random'


    @classmethod
    async def define_word(cls, word):
        res = await cls._get_word(word)
        new_res = cls._extract_definitions(res)
        return new_res

    @classmethod
    async def random_word(cls):
        res = await cls._random_word()
        new_res = cls._extract_definitions(res)
        new_res = html.unescape(new_res)
        return new_res


    @classmethod
    async def _get_word(cls, word):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.urbandictionary.com/v0/define?term={word}") as resp:
                result = await resp.json()
                return result

    @classmethod
    async def _random_word(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.RANDOM_URL) as resp:
                result = await resp.json()
                return result


    @classmethod
    def _extract_definitions(cls, some_result):
        result = some_result['list']
        text = ""
        # dict_keys(['definition', 'word', 'defid', 'example'])
        for defin in result:
            text += f"{defin['definition']}\n{defin['example']}"
        return text


if __name__ == "__main__":
    async def main():
        x = await UrbanDicAPI.random_word()
        print(x)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
