import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        # async with session.get(
        #         'http://127.0.0.1:8080/post/1'
        #
        # ) as response:
        #     print(await response.text())

        async with session.post(
                'http://127.0.0.1:8080/post/',
                json={"title": "test_post_1", "description": "meow_meow", "owner_name": "Yar"}

        ) as response:
            print(await response.text())
        # async with session.delete(
        #         'http://127.0.0.1:8080/post/1'
        #
        # ) as response:
        #     print(await response.text())


asyncio.run(main())
