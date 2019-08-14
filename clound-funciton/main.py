from aiohttp import web
import asyncio, asyncssh, sys

async def foo():
    return 'Asynchronicity! TWO'

async def bar():
    return await foo()


async def hello():
    try:
        # asyncio.get_event_loop().run_until_complete(run_client())
        await run_client()
        return 'YAY'
    except (OSError, asyncssh.Error) as exc:
        sys.exit('SSH connection failed: ' + str(exc))
        return 'NAY'

async def run_client():
    print("RUNNING IT")
    async with asyncssh.connect('75.71.20.33', 2222, username='pi', known_hosts=None, password='DvyN4RG^s6',) as conn:
        result = await conn.run('python doorajar/switcher.py', check=True)
        #DvyN4RG^s6
        print(result.stdout, end='')
        return web.Response(text="Lightup")

def test(request):
    # return null
    return asyncio.run(hello())