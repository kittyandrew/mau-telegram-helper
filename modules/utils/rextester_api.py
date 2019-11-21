import aiohttp


class RexTesterAPI:

    LANGUAGES = {"c#": 1,
                "vb.net": 2,
                "f#": 3,
                "java": 4,
                "python": 5,
                "c (gcc)": 6,
                "c++ (gcc)": 7,
                "php": 8,
                "pascal": 9,
                "objective-c": 10,
                "haskell": 11,
                "ruby": 12,
                "perl": 13,
                "lua": 14,
                "nasm": 15,
                "sql server": 16,
                "javascript": 17,
                "lisp": 18,
                "prolog": 19,
                "go": 20,
                "scala": 21,
                "scheme": 22,
                "node.js": 23,
                "python3": 24,
                "octave": 25,
                "c (clang)": 26,
                "c++ (clang)": 27,
                "c++ (vc++)": 28,
                "c (vc)": 29,
                "d": 30,
                "r": 31,
                "tcl": 32,
                "mysql": 33,
                "postgresql": 34,
                "oracle": 35,
                "swift": 37,
                "bash": 38,
                "ada": 39,
                "erlang": 40,
                "elixir": 41,
                "ocaml": 42,
                "kotlin": 43,
                "brainfuck": 44,
                "fortran": 45,}


    def __init__(self):
        pass

    @classmethod
    async def execute(cls, text, lang="py3"):
        lang, lang_num = cls._determine_lang_num(lang)

        result = await cls.post_language(lang_num, text)
        result_stringified = cls._pretty_stringify(result)
        super_result = f"```\nLanguage:```{lang}```\nCode:```{text}{result_stringified}"
        error = cls._raise_too_long_message(super_result)
        if error[0]:
            super_result = f"```\nLanguage:```{lang}```\nCode:```{text}```\nError:```Too long result ({error[1]} characters)"

        return super_result

    @classmethod
    async def post_language(cls, lang, text):
        async with aiohttp.ClientSession() as session:
            payload = {'LanguageChoice': lang, 'Program': text, }
            async with session.post('https://rextester.com/rundotnet/api', data=payload) as resp:
                result = await resp.json()
                return result


    @classmethod
    def _pretty_stringify(cls, text):
        errors = text['Errors']
        result = text['Result']
        stats = text['Stats']
        try:
            n_stats = stats.split(",")
            new_stats = []
            for x in n_stats:
                x = x.split(":")
                for each in x:
                    new_stats.append(each)
            n_stats = [x for x in new_stats[1::2]]
            stats = n_stats
        except Exception as e:
            print(e)
        try:
            stats = f"Running time:{stats[0]}\nCPU time:{stats[1]}\nMemory usage:{stats[2]}"
        except:
            stats = text['Stats']
        if errors is None:
            text = f"```\nResult:```{result}```\nStats:```{stats}"
        else:
            text = f"```\nResult:```{result}```\nError:```{errors}```\nStats:```{stats}"
        return text


    @classmethod
    def _determine_lang_num(cls, name):
        name = name.lower()

        if name == "py3":
            name = "python3"
        elif name == "py":
            name = "python"
        elif name == "js":
            name = "javascript"
        elif name == "c":
            name = "c (gcc)"
        elif name == "c++":
            name = "c++ (gcc)"
        elif name == "obj-c":
            name = "objective-c"

        return name, cls.LANGUAGES[name]


    @classmethod
    def _raise_too_long_message(cls, text):
        x = len(text)
        if x >= 4096:
            return True, x
        else:
            return False, x


if __name__ == "__main__":
    pass

