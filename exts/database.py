import aiosqlite


class AioDbClass:

    def __init__(self, db_path: str) -> None:
        self.path = db_path

    async def execute(self, code: str) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(code)

    async def execute_args(self, code: str, args: tuple) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(code, args)

    async def select(self, code: str, fetch: str):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(code) as cursor:
                if fetch == "one":
                    return await cursor.fetchone()

                elif fetch == "all":
                    return await cursor.fetchall()

                else:
                    raise ValueError(f'the "fetch" argument must be "all" or "one" not {fetch}')

    async def select_args(self, code: str, args: tuple, fetch: str):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(code, args) as cursor:
                if fetch == "one":
                    return await cursor.fetchone()

                elif fetch == "all":
                    return await cursor.fetchall()

                else:
                    raise ValueError(f'the "fetch" argument must be "all" or "one" not {fetch}')