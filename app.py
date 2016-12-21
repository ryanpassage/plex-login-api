from flask import Flask, jsonify, request, redirect
import pymssql, os

DBSERVER = os.environ.get('PLEXAPI_SERVER', 'database1.cmwa.local')
DATABASE = os.environ.get('PLEXAPI_DB', 'PlexKioskAPI')
DBUSER = os.environ.get('PLEXAPI_USER', 'plexkiosk')
DBPASSWORD = os.environ.get('PLEXAPI_PW')

application = Flask(__name__)
application.config.from_object(__name__)
application.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET')


@application.route("/")
def index():
	response = jsonify({'success': True})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@application.route("/ext")
def extension():
	return redirect("https://chrome.google.com/webstore/detail/perplexed-cmwa-plex-enhan/icjkboalmbbioijkjngdggmncceajali?hl=en-US&gl=US")

@application.route("/get/<int:member>/<int:badge>")
def test(member, badge):
	data = {'success': False}

	# poor-man's security check
	#if '192.168.140.' not in request.remote_addr:
	#	data['error'] = 'Restricted.'
	#	return jsonify(data)

	member_number = member
	badge_number = badge

	with pymssql.connect(DBSERVER, DBUSER, DBPASSWORD, DATABASE) as conn:
		with conn.cursor(as_dict=True) as db:

			db.execute('select * from plex_logins where badge_number=%s and member_number=%s', (badge_number, member_number))

			for row in db:
				data['login'] = row	
				data['success'] = True

			if not data['success']:
				data['error'] = 'No CMWA logins found with that member number and badge combination.';

	response = jsonify(data)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)

