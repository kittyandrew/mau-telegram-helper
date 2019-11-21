"""
KExec
Easily execute inputted code
By Kat Hamer

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright (c) 2019 Katelyn Hamer
"""

import asyncio  # Work with async
import contextlib  # Use IO redirection context manager
import io  # Work with StringIO objects
import traceback  # Handle and format tracebacks
import datetime # For finding time of operation

def add_line_numbers(text: str, pad_amount=2) -> str:
    """Add line numbers to text"""
    numbered_text = ""  # Placeholder to store numbered text
    for index, line in enumerate(text.split("\n")[:-1]):  # Iterate through each line of the code
        line_number = str(index).zfill(pad_amount)  # Pad the line number with 0s, e.g. 1 = 01 or 001
        numbered_text += f"{line_number}: {line}\n"  # Format the text line e.g. 01: print("hello")
    return numbered_text


def wrap_code(code: str, indent_amount=4) -> str:
    """Wrap code inside a function"""
    wrapper = f"async def __ex(c, e):"  # Coroutine definition
    indented_code = "\n".join(["    "+line for line in code.split("\n")])  # Indent each line of code
    return f"{wrapper}\n{indented_code}"  # Concatenate the wrapper and the indented code


def output_log(code: str, output: str, result: str, exception_info: tuple):
    """Display a formatted report of code execution"""
    numbered_code = add_line_numbers(code)  # Number the code
    print(f"Code:\n{numbered_code}")

    if output:  # If there is output, display it
        print(f"Output:\n{output}")

    if result:  # If the coroutine returned a value, display it
        print(f"Returned:\n{result}")

    if exception_info:  # If there was an exception, display a traceback
        print(f"Exceptions:\n{exception_info}")

    if not result and not output:  # If nothing was outputted or returned, display a message
        print("Nothing returned or outputted.")


async def evaluate(code: str, c, e) -> tuple:
    """Evaluate code"""
    wrapped = wrap_code(code)  # Wrap code in an asynchronous function

    output = io.StringIO()  # Initialise a new StringIO object to buffer output
    with contextlib.redirect_stdout(output):  # Redirect all output to our StringIO buffer
        try:  # Try to execute the code
            exec(wrapped)  # Execute the wrapped code which stores a coroutine in locals
            coroutine = locals()["__ex"]  # Get the coroutine from locals

            result = await coroutine(c, e)  # Await the wrapper coroutine and get it's return value
            exception_info = None  # Set exception info to None since no exception happened
        except Exception:  # Catch any exception that happens within the code
            exception_info = traceback.format_exc()  # Store traceback information inside a variable
            result = None  # Set the result value to None to avoid a NameError

    return code, output.getvalue(), result, exception_info



# Very strange fast-made class for executor to be one-liner
class KExec:

    def __init__(self, user_input:str):
        self.user_input = user_input

    def __str__(self):
        result = ""
        if self.code:
            result += f"**Code: **\n`{self.code}`\n\n"
        if self.output:
            result += f"**Result: **\n`{self.output}`\n\n"
        if self.result:
            result += f"**Returned: **\n`{self.result}`\n\n"
        if self.exception_info:
            result += f"**Error: **\n`{self.exception_info}`\n\n"

        result += f"**Runtime: **\n`{self.timetaken}`"
        return result

    async def eval(self, c: "Client of Telethon lib", e: "Event of Telethon lib"):
        date1 = datetime.datetime.now()
        self.code, self.output, self.result, self.exception_info = await evaluate(self.user_input, c, e)
        date2 = datetime.datetime.now()
        self.timetaken = (date2 - date1).total_seconds()
        return self # Just to do it one-line with creating class


def main():
    """Test function"""
    inputted_code = []  # Store inputted lines in an array to join later
    user_input = "."  # Set user input to non empty by default
    print("Enter code to evaluate.")
    print("Empty line finishes input.")
    while not user_input == "":  # Loop until an empty line is entered
        user_input = input(">>> ")
        inputted_code.append(user_input)  # Append inputted line to input array
    formatted_code = "\n".join(inputted_code)  # Seperate each line with a newline

    loop = asyncio.get_event_loop()  # Get current event loop
    code, output, result, exception_info = loop.run_until_complete(evaluate(formatted_code))  # Evaluate code

    output_log(code, output, result, exception_info)  # Display a log


if __name__ == "__main__":
    async def main():
        myinput = "print(5)\nprint(10)\nawait asyncio.sleep(5)\nprint('KEK')"
        executor = await KExec(myinput).eval()
        print(executor)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
    #main()  # Run main function
