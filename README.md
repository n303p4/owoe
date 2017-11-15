# owoe
A dead simple aiohttp-based library for weeb.sh. Nothing more. Honest.

Still under construction, moving along.

## Installation

In a terminal on Linux, type:
```bash
python3 -m pip install git+https://github.com/n303p4/owoe#egg=owoe
```
For Windows, you may have to type out the entire path to your Python
executable, but the procedure is otherwise the same.

## Usage

A simple and bad example:
```py
#!/usr/bin/env python3

import asyncio

import aiohttp
import owoe

my_loop = asyncio.get_event_loop()
my_session = aiohttp.ClientSession(loop=my_loop)
my_owoe = owoe.Owoe(token=input("Enter your token here: "), session=my_session)

async def main():
    await my_owoe.update_image_types()
    print("Available types:", ", ".join(my_owoe.types))
    type_input = input("Enter a type here: ")
    image_url = await my_owoe.random_image(type_=type_input)
    print("Got image link:", image_url)
    my_session.close()

my_loop.run_until_complete(main())
```