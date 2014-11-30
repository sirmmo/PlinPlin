from bottle import route, run, template, request

import redis

import json

r = redis.Redis()

@route('/')
def index():
	return "template"

@route('/status')
def index():
	k = r.keys()
	return json.dumps(k)

@route('/out')
def put():
	tup = request.params.get("tuple")
	tup = json.loads(tup)
	tup = setup_tuple(tup)
	return do_put(tup)

@route('/in')
def get():
	tup = request.params.get("tuple")
	tup = json.loads(tup)
	tup = setup_tuple(tup)
	return json.dumps(do_get(tup))

@route('/rd')
def read():
	tup = request.params.get("tuple")
	tup = json.loads(tup)
	tup = setup_tuple(tup)
	return json.dumps(do_get(tup, True))

def do_put(tup):
	r.set(tup,"1")
	return "ok"

def do_get(tup, read=False):
	matches = r.keys(tup)
	to_return = None
	if len(matches) > 0:
		to_return = matches[0]
		if not read:
			r.delete(matches[0])
	return from_string(to_return)

def setup_tuple(tup):
	print tup
	new_tup = []
	if type(tup) == list:
		for t in tup:
			new_tup.append(setup_tuple(t))
	else:
		new_tup = "%s:%s" % (tup.get("t"), tup.get("v"))
		return new_tup
	return "|".join(new_tup)

def from_string(tup):
	if tup:
		return [{"t":p.split(":")[0], "v":p.split(":")[1]}for p in tup.split("|")]
	else:
		return None

if __name__=="__main__":
	run(host='0.0.0.0', port=4124, debug=True)