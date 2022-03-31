from functions import make_keychain, write_to_csv, print_instructions
import sys

try:
	if sys.argv[1].endswith('.csv'):
		csv_file = sys.argv[1]
		keychain = make_keychain(csv_file)
		write_to_csv(keychain)
		print(f"Created {len(keychain)} keychain passwords.")

	else:
		print_instructions()

except:
	print_instructions()