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
```
# Clone this repo
git clone https://github.com/rotyflo/import2keychain.git ~/import2keychain

# Move into folder
cd ~/import2keychain

# Run application
python3 import2keychain.py /path/to/bitwarden_passwords.csv
```

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details