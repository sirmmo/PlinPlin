from bottle import route, run, template, request
import redis
import json
import ConfigParser
import uuid

r = redis.Redis()

conf = ConfigParser.ConfigParser()
conf.read("config.ini")

UUID_DIVIDER = conf.get("global","uuid_divider") if conf.has_option("global", "uuid_divider") else "$#$"
TUPLE_DIVIDER = conf.get("global","tuple_divider") if conf.has_option("global", "tuple_divider") else "_|_"
PART_DIVIDER = conf.get("global","part_divider") if conf.has_option("global", "part_divider") else ":::"

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
	tup = "*%s%s" % (UUID_DIVIDER, tup.split(UUID_DIVIDER)[1])
	print tup
	matches = r.keys(tup)
	to_return = None
	if len(matches) > 0:
		to_return = matches[0]
		if not read:
			r.delete(matches[0])
	return from_string(to_return)

def setup_tuple(tup):
	new_tup = []
	if type(tup) == list:
		for t in tup:
			new_tup.append(setup_tuple(t))
	else:
		new_tup = "%s%s%s" % (tup.get("t"), PART_DIVIDER, tup.get("v"))
		return new_tup
	return str(uuid.uuid4()) + UUID_DIVIDER + TUPLE_DIVIDER.join(new_tup)

def from_string(tup):
	if tup:
		tup = tup.split(UUID_DIVIDER)[1]
		return [{"t":p.split(PART_DIVIDER)[0], "v":p.split(PART_DIVIDER)[1]}for p in tup.split(TUPLE_DIVIDER)]
	else:
		return None

if __name__=="__main__":
	run(host=conf.get("global","bind"), port=conf.getint("global","port"))