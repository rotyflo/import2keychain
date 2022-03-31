from functions import *
import csv
import sys

try:
	if sys.argv[1].endswith('.csv'):
		keychain_passwords = []

		with open(sys.argv[1]) as bitwarden_passwords:
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
				keychain_passwords.append(keychain_pw)
	
		headers = keychain_passwords[0].keys()
		with open('keychain_passwords.csv', 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = headers)
			writer.writeheader()
			writer.writerows(keychain_passwords)

		print(f"Created {len(keychain_passwords)} keychain passwords.")

	else:
		print_instructions()

except:
	print_instructions()