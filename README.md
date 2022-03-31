# Import2Keychain
Properly move all of your passwords into keychain.
Keep your notes, fields and TOTPs too!

Note: Don't forget to export your organizations as well.

## Getting Started

### Prerequisites
```
# Install Brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python3
brew install python
```

### Usage
1. Log in to bitwarden.com

2. Tools > Export Vault

3. Select .csv as file format and export vault

4. Settings > Organizations

5. Repeat steps 2 and 3 for each organization

6. Clone this repo

`git clone https://github.com/rotyflo/import2keychain.git ~/import2keychain`

7. Move into folder

`cd ~/import2keychain`

8. Run app on each csv file that was exported

`python3 import2keychain.py /path/to/bitwarden_passwords.csv`

9. On MacOS, go to System Preferences > Passwords

10. Open the dropdown menu near the bottom-left corner and select Import Passwords

11. Import the csv files that were exported from this app

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details