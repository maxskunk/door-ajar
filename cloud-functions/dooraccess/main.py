from aiohttp import web
from flask import jsonify, abort, escape
import asyncio, asyncssh, sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, date
import pytz
import os

utc=pytz.UTC

PROJECT_ID = 'zokya-media'

cred = credentials.ApplicationDefault()
default_app = firebase_admin.initialize_app(cred, {
	'projectId': PROJECT_ID,
})
db = firestore.client()

async def trigger_switcher():
    try:
        # asyncio.get_event_loop().run_until_complete(run_client())
        await run_client()
        return 200
    except (OSError, asyncssh.Error) as exc:
        sys.exit('SSH connection failed: ' + str(exc))
        return 500

async def run_client():
    print("RUNNING IT NOW")
    async with asyncssh.connect(os.environ.get('PI_IP_ADDRESS', ''), 2222, username='pi', known_hosts=None, password=os.environ.get('PI_PASSWORD', ''),) as conn:
        result = await conn.run('python doorajar/switcher.py', check=True)
        print(result.stdout, end='')
        return web.Response(text="Lightup")

def test_firestore(request):
	request_json = request.get_json(silent=True)
	request_args = request.args

	if request_json and 'key' in request_json:
		key = request_json['key']
	elif request_args and 'key' in request_args:
		key = request_args['key']
	else:
		key = None
	docs = db.collection(u'valid_door_keys').where(u'key', u'==', key).stream()
	verdict = False
	for doc in docs:
		verdict = doc.to_dict()['key'] == key
		if verdict:
			now = datetime.now()
			expired = doc.to_dict()['expiration'].replace(tzinfo=utc) < now.replace(tzinfo=utc)
			if expired:
				return ('Key Expired',401)
        
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
		return ('',204,headers)

    # Set CORS headers for the main request
	headers = {
		'Access-Control-Allow-Origin': '*'
	}

	if verdict:
#		return ('Correct Key',200,headers)
		
		status = asyncio.run(trigger_switcher())
		if(200):
			# asyncio.get_event_loop().run_until_complete(run_client())
			return ('Success',200,headers)
		else:
			return ('Error Contacting Switcher',500,headers)
	else:
		return ('Incorrect Key',401,headers)
		

#	existing_posts = db.collection(u'valid_door_keys')
#	existing_posts.where(u'key', u'==', u'lalala')
#	return jsonify(request)
#	for post in existing_posts:
#		print('squeeze')


#	return 'bannana' #jsonify(existing_posts[0].to_dict())
# doc_ref = db.collection('valid_door_keys').document('pNjd1DRMfo1983qPrWq2')
# docs = db.collection('valid_door_keys').where('key', '==', 'lalala').stream()
# query_ref = cities_ref.where('key', '==', 'lalala')

#    doc = query_ref.get()
#    if True:
#		return 'goose'
#		return '{} => {}'.format(doc.id, doc.to_dict())
#        return str('lalala' in doc.to_dict().values())
#        return jsonify(doc.to_dict())
#	else:
#        return 'shit broke'
#    else:
#        doc_ref.set({'name': 'Hello'})
#        return 'UPDATED'


def test(request):
	# return null
    # return asyncio.run(hello())
    return "POOP 5"
	#keys_ref = db.collection(u'valid_door_keys')
	# docs = keys_ref.stream()

#users_ref = db.collection(u'users')
#docs = users_ref.stream()

#for doc in docs:
#    print(u'{} => {}'.format(doc.id, doc.to_dict()))
# valid_door_keys