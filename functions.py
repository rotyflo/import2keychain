import csv

def print_instructions():
	print('Usage: python3 import2keychain.py /path/to/bitwarden_passwords.csv')


def require_url(url, name):
	placeholder = f"https://{name.replace(' ', '_').lower()}.save/"
	return placeholder if url == '' else url


def require_username(username, name):
	return name if username == '' else username


def require_password(password):
	return ' ' if password == '' else password


def get_slash_indices(url):
	url = url + '/'
	return [i for i in range(len(url)) if url[i] == '/']


def get_site(url):
	slash_indices = get_slash_indices(url)
	return url[slash_indices[1] + 1:slash_indices[2]]


def make_title(url, username):
	site = get_site(url)
	return f"{site} ({username})"


def make_url(url):
	slash_indices = get_slash_indices(url)
	return url[:slash_indices[2] + 1]


def make_notes(*args):
	valid_parts = filter(lambda arg: arg != '', args)
	formatted_parts = map(lambda part: part + '\n\n', valid_parts)
	return ''.join(formatted_parts)


def make_otpauth(url, username, otp):
	if otp == '': return ''
	site = get_site(url)
	user = username.replace(' ', '%20')
	otpkey = otp.replace(' ', '').upper()
	return f"otpauth://totp/{site}:{user}?secret={otpkey}&issuer={site}&algorithm=SHA1&digits=6&period=30"


def make_keychain_pw(bw):
	return {
		'Title': make_title(bw['login_uri'], bw['login_username']),
		'URL': make_url(bw['login_uri']),
		'Username': bw['login_username'],
		'Password': bw['login_password'],
		'Notes': make_notes( bw['name'],  bw['notes'], bw['fields']),
		'OTPAuth': make_otpauth( bw['login_uri'], bw['login_username'], bw['login_totp'])
	}


def make_keychain(csv_file):
	keychain = []

	with open(csv_file) as bitwarden_passwords:
		for bitwarden in csv.DictReader(bitwarden_passwords):
			bitwarden['login_uri'] = require_url(
				bitwarden['login_uri'],
				bitwarden['name']
			)
			bitwarden['login_username'] = require_username(
				bitwarden['login_username'], 
				bitwarden['name']
			)
			bitwarden['login_password'] = require_password(
				bitwarden['login_password']
			)

			keychain_pw = make_keychain_pw(bitwarden)
			keychain.append(keychain_pw)

	return keychain


def write_to_csv(keychain):
	headers = keychain[0].keys()

	with open('keychain_passwords.csv', 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = headers)
		writer.writeheader()
		writer.writerows(keychain)