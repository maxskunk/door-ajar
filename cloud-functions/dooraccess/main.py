from aiohttp import web
import asyncio
import asyncssh
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import pytz
import os
import json
# from flask import jsonify

utc = pytz.UTC

cred = credentials.ApplicationDefault()
default_app = firebase_admin.initialize_app(cred, {
    'projectId': os.environ.get('PROJECT_ID', ''),
})
db = firestore.client()


async def trigger_switcher():
    try:
        await run_client()
        return 200
    except (OSError, asyncssh.Error) as exc:
        sys.exit('SSH connection failed: ' + str(exc))
        return 500


async def run_client():
    async with asyncssh.connect(os.environ.get('PI_IP_ADDRESS', ''), 2222, username='pi', known_hosts=None, password=os.environ.get('PI_PASSWORD', ''),) as conn:
        result = await conn.run('python doorajar/switcher.py', check=True)
        print(result.stdout, end='')
        return web.Response(text="Lightup")


def test_firestore(request):

    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'key' in request_json:
        key = request_json['key']
    elif request_args and 'key' in request_args:
        key = request_args['key']
    else:
        key = None

    if request_json and 'wakeup' in request_json:
        wakeup = request_json['wakeup']
    elif request_args and 'wakeup' in request_args:
        wakeup = request_args['wakeup']
        if wakeup == "True" or wakeup == "true":
            wakeup = True
        else:
            wakeup = False
    else:
        wakeup = False

    docs = db.collection(u'valid_door_keys').where(u'key', u'==', key).stream()
    verdict = False
    for doc in docs:
        verdict = doc.to_dict()['key'] == key
        if verdict:
            now = datetime.now()
            print("TEST: " + str(doc.to_dict()))
            expired = doc.to_dict()['expiration'].replace(
                tzinfo=utc) < now.replace(tzinfo=utc)
            not_valid = doc.to_dict()['inception'].replace(
                tzinfo=utc) > now.replace(tzinfo=utc)
            if not_valid:
                return (json.dumps({'msg': 'Key not yet valid'}), 412, headers)
            if expired:
                return (json.dumps({'msg': 'Key Expired'}), 401, headers)

    if verdict:
        if wakeup:
            return (json.dumps({'msg': 'The Function is Now Awake'}), 200, headers)
        try:
            asyncio.run(trigger_switcher())
            return (json.dumps({'msg': 'Door Open Success'}), 200, headers)
        except Exception as e:
            return (json.dumps({'msg': 'Could Not Contact Switcher: '+e}), 500, headers)
    else:
        return (json.dumps({'msg': 'Incorrect key'}), 401, headers)
