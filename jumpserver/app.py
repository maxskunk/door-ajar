from aiohttp import web
import asyncio, asyncssh, sys

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

@routes.get('/gogo')
async def hello(request):
    try:
        # asyncio.get_event_loop().run_until_complete(run_client())
        await run_client()
        return web.Response(text="REturn")
    except (OSError, asyncssh.Error) as exc:
        sys.exit('SSH connection failed: ' + str(exc))
        return web.Response(text="Lightup Fail")
    

async def run_client():
    print("RUNNING IT")
    async with asyncssh.connect('75.71.20.33', 2222, username='pi', known_hosts=None, PASSWORD,) as conn:
        result = await conn.run('python doorajar/switcher.py', check=True)
        #DvyN4RG^s6
        print(result.stdout, end='')
        return web.Response(text="Lightup")

app = web.Application()
app.add_routes(routes)
web.run_app(app)