import csv
import sys

passwords = []

with open(sys.argv[1]) as data:
	for dictionary in csv.DictReader(data):
		bitwarden_passwords = dictionary

		# Fix for url undefined
		if bitwarden_passwords['login_uri'] == '':
			bitwarden_passwords['login_uri'] = 'https://undefined.undefined/'

		if bitwarden_passwords['login_username'] == '':
			bitwarden_passwords['login_username'] = 'undefined'

		if bitwarden_passwords['login_password'] == '':
			bitwarden_passwords['login_password'] = 'undefined'
		
		# Fix for trailing slash missing bug
		bitwarden_passwords['login_uri'] = bitwarden_passwords['login_uri'] + '/'

		def get_slash_indices(url):
			return [i for i in range(len(url)) if url[i] == '/']

		def make_title(url, username):
			slash_indices = get_slash_indices(url)
			site = url[slash_indices[1] + 1:slash_indices[2]]
			return f"{site} ({username})"

		def make_url(url):
			slash_indices = get_slash_indices(url)
			return url[:slash_indices[2] + 1]

		def make_otpauth(url, username, otp):
			if otp == '': return ''

			slash_indices = get_slash_indices(url)
			site = url[slash_indices[1] + 1:slash_indices[2]]
			user = username.replace(' ', '%20')
			otpkey = otp.replace(' ', '').upper()
			return f"otpauth://totp/{site}:{user}?secret={otpkey}&issuer={site}&algorithm=SHA1&digits=6&period=30"

		def make_notes(notes, fields, otp):
			parts = []
			if notes != '':
				parts.append(f"Notes:\n{notes}\n\n")
			if fields != '':
				parts.append(f"Fields:\n{fields}\n\n")
			if otp != '':
				parts.append(f"OTP:\n{otp}\n\n")
			if parts == []:
				return ''
			else:
				return ''.join(parts)

		keychain_passwords = {
			'Title': make_title(bitwarden_passwords['login_uri'], bitwarden_passwords['login_username']),
			'URL': make_url(bitwarden_passwords['login_uri']),
			'Username': bitwarden_passwords['login_username'],
			'Password': bitwarden_passwords['login_password'],
			'Notes': make_notes(bitwarden_passwords['notes'], bitwarden_passwords['fields'], bitwarden_passwords['login_totp']),
			'OTPAuth': make_otpauth(bitwarden_passwords['login_uri'], bitwarden_passwords['login_username'], bitwarden_passwords['login_totp'])
		}

		passwords.append(keychain_passwords)


headers = ['Title', 'URL', 'Username', 'Password', 'Notes', 'OTPAuth']

with open('keychain_passwords.csv', 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = headers)
	writer.writeheader()
	writer.writerows(passwords)