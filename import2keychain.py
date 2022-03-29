import csv
import sys

if sys.argv[1] == '--help':
	print('Usage: python3 app.py /path/to/passwordsbackup.csv')

if sys.argv[1].endswith('.csv'):
	passwords = []

	with open(sys.argv[1]) as data:
		for dictionary in csv.DictReader(data):
			bitwarden_passwords = dictionary

			# Fix for url undefined
			if bitwarden_passwords['login_uri'] == '':
				bitwarden_passwords['login_uri'] = f"https://{bitwarden_passwords['name'].replace(' ', '_').lower()}.save/"

			if bitwarden_passwords['login_username'] == '':
				bitwarden_passwords['login_username'] = bitwarden_passwords['name']

			if bitwarden_passwords['login_password'] == '':
				bitwarden_passwords['login_password'] = ' '
			
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

			def make_notes(name, notes, fields, otp):
				parts = []
				if name != '':
					parts.append(f"{name}\n\n")
				if notes != '':
					parts.append(f"{notes}\n\n")
				if fields != '':
					parts.append(f"{fields}\n\n")
				if otp != '':
					parts.append(f"OTP: {otp}\n\n")
				if parts == []:
					return ''
				else:
					return ''.join(parts)

			keychain_passwords = {
				'Title': make_title(bitwarden_passwords['login_uri'], bitwarden_passwords['login_username']),
				'URL': make_url(bitwarden_passwords['login_uri']),
				'Username': bitwarden_passwords['login_username'],
				'Password': bitwarden_passwords['login_password'],
				'Notes': make_notes(bitwarden_passwords['name'], bitwarden_passwords['notes'], bitwarden_passwords['fields'], bitwarden_passwords['login_totp']),
				'OTPAuth': make_otpauth(bitwarden_passwords['login_uri'], bitwarden_passwords['login_username'], bitwarden_passwords['login_totp'])
			}

			passwords.append(keychain_passwords)

	backups = {
		'Title': 'backup.save ( )',
		'URL': 'https://backup.save/',
		'Username': 'Backup',
		'Password': ' ',
		'Notes': f"{passwords}",
		'OTPAuth': ''
	}

	passwords.append(backups)

	headers = ['Title', 'URL', 'Username', 'Password', 'Notes', 'OTPAuth']

	with open('keychain_passwords.csv', 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = headers)
		writer.writeheader()
		writer.writerows(passwords)

else:
	print('Usage: python3 app.py /path/to/passwordsbackup.csv')