import aiomysql

from config import Config as c

from . import console

POOL = None


async def create_pool(loop):
    console.info('creating connection pool')
    global POOL
    POOL = await aiomysql.create_pool(
        host=c.DB_HOST,
        port=c.DB_PORT,
        user=c.DB_USER,
        db=c.DB_NAME,
        password=c.DB_PASS,
        program_name='alttprbot',
        charset='utf8mb4',
        autocommit=True,
        maxsize=10,
        minsize=1,
        loop=loop
    )


async def select(sql, args=None, size=None):
    global POOL
    if args is None:
        args = []
    with (await POOL) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = await cur.fecthmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        return rs


async def execute(sql, args=None):
    global POOL
    if args is None:
        args = []
    with (await POOL) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
        except BaseException as err:
            raise
        return affected
