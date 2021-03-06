#!/usr/bin/env python3

"""A dead simple aiohttp-based library for weeb.sh. Nothing more. Honest."""

from typing import List

import urllib
import asyncio

import aiohttp

BASE_URL_TYPES = "https://api.weeb.sh/images/types"
BASE_URL_TAGS = "https://api.weeb.sh/images/tags"
BASE_URL_RANDOM = "https://api.weeb.sh/images/random?{0}"


class Owoe:
    """A class that contains a simple interface for weeb.sh.

    This will typically be used compositionally, as a component of a larger class.
    """

    def __init__(self, token: str=None, session: aiohttp.ClientSession=None):
        """Constructor method for `Owoe`.

        * `token` - An `str` containing your token from Wolke.
        * `session` - An optional `aiohttp.ClientSession` to use Owoe with another program. If
                      not supplied, Owoe will create one for itself to be used standalone.

        **Fields not in the constructor**

        * `types` - A `list` of `str` containing all valid image types. It's recommended not to
                    update this yourself; instead, call `update_image_types()`.
        * `tags` - A `list` of `str` containing all valid image tags. It's recommended not to
                   update this yourself; instead, call `update_image_tags()`.
        * `headers` - A `dict` for simple HTTP authorization.
        """
        self.token = token
        self.headers = {"Authorization": f"Wolke {token}"}
        self.types = []
        self.tags = []
        if not session:
            loop = asyncio.get_event_loop()
            self.session = aiohttp.ClientSession(loop=loop)
        else:
            self.session = session

    async def update_image_types(self):
        """Update the image types `list` by calling the `/types` endpoint. This is a coroutine.

        You must call this to populate the types `list`.

        If successful, returns a `None`, otherwise returns an `int` with an HTTP status code.
        """
        async with self.session.get(BASE_URL_TYPES, headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                types = data["types"]
                self.types = []
                for type_ in types:
                    self.types.append(type_)
                return
            return response.status

    async def update_image_tags(self):
        """Update the image tags `list` by calling the `/tags` endpoint. This is a coroutine.

        You must call this to populate the tags `list`.

        If successful, returns a `None`, otherwise returns an `int` with an HTTP status code.
        """
        async with self.session.get(BASE_URL_TAGS, headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                tags = data["tags"]
                self.tags = []
                for tag in tags:
                    self.tags.append(tag)
                return
            return response.status

    async def random_image(self, type_: str=None, tags: List[str]=[]):
        """Get a random image from weeb.sh by calling the `/random` endpoint. This is a coroutine.

        Possible return values are as follows:

        * If successful, returns an `str` with the URL of the image.
        * If an HTTP status error occurs, returns an `int` with the status code.

        * `type_` - An `str` representing the type of the image to be obtained.
                    Must be in `self.types`. Has an underscore to avoid colliding with
                    built-in Python `type`.
        * `tags` - A `list` of `str` to use in the image search.
        """
        parameters_url = {}
        if type_:
            parameters_url["type"] = type_
        if tags:
            parameters_url["tags"] = urllib.parse.quote_plus(" ".join(tags))

        parameters_url = urllib.parse.urlencode(parameters_url)

        url_random = BASE_URL_RANDOM.format(parameters_url)

        async with self.session.get(url_random, headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                url_image = data["url"]
                return url_image
            return response.status
