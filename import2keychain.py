import csv
import sys

instructions = '''Usage: python3 import2keychain.py /path/to/bitwarden_passwords.csv'''

try:
	if sys.argv[1].endswith('.csv'):
		passwords = []

		with open(sys.argv[1]) as bitwarden_passwords:
			for bitwarden in csv.DictReader(bitwarden_passwords):
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

				def make_otpauth(url, username, otp):
					if otp == '': return ''
					site = get_site(url)
					user = username.replace(' ', '%20')
					otpkey = otp.replace(' ', '').upper()
					return f"otpauth://totp/{site}:{user}?secret={otpkey}&issuer={site}&algorithm=SHA1&digits=6&period=30"

				def make_notes(*args):
					valid_parts = filter(lambda arg: arg != '', args)
					formatted_parts = map(lambda part: part + '\n\n', valid_parts)
					return ''.join(formatted_parts)

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

				keychain_pw = {
					'Title': 
						make_title(
							bitwarden['login_uri'],
							bitwarden['login_username']
						),
					'URL':
						make_url(bitwarden['login_uri']),
					'Username':
						bitwarden['login_username'],
					'Password':
						bitwarden['login_password'],
					'Notes':
						make_notes(
							bitwarden['name'], 
							bitwarden['notes'],
							bitwarden['fields']
						),
					'OTPAuth': 
						make_otpauth(
							bitwarden['login_uri'],
							bitwarden['login_username'],
							bitwarden['login_totp']
						)
				}

				passwords.append(keychain_pw)
	
		headers = passwords[0].keys()
		with open('keychain_pw.csv', 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = headers)
			writer.writeheader()
			writer.writerows(passwords)

	else:
		print(instructions)

except:
	print(instructions)