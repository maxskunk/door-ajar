import asyncio, asyncssh, sys

async def run_client():
    async with asyncssh.connect('192.168.0.222', username='pi', known_hosts=None, password='DvyN4RG^s6') as conn:
        result = await conn.run('python doorajar/switcher.py', check=True)
        #DvyN4RG^s6
        print(result.stdout, end='')

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))