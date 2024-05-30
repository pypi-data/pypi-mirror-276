# CHARS

chars is a simple Python package that provides functions to get different sets of characters including uppercase letters, lowercase letters, numbers, and special characters.

## Features

- Retrieve uppercase letters
- Retrieve lowercase letters
- Retrieve numbers
- Retrieve special characters
- Retrieve a combination of all character sets

## Installation

You can install the package using `pip3`:

```sh
pip3 install chars
```

## Usage

### Importing the Package
To use the functions provided by the package, you first need to import the `chars` module:

```sh
from mypackage import chars
```

### Retrieving Uppercase Letters
You can retrieve all uppercase letters using the uppercase function:

```sh
uppercase_chars = chars.uppercase()
print(uppercase_chars)
# Output: ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

### Retrieving Lowercase Letters
To get all lowercase letters, use the lowercase function:

```sh
lowercase_chars = chars.lowercase()
print(lowercase_chars)
# Output: abcdefghijklmnopqrstuvwxyz
```

### Retrieving Numbers
If you need all numeric characters, use the numbers function:

```sh
numbers = chars.numbers()
print(numbers)
# Output: 1234567890
```

### Retrieving Special Characters
For special characters, use the specialchars function:

```sh
special_chars = chars.specialchars()
print(special_chars)
# Output: ~`!@#$%^&*()-_=+|[]\{|};':",./<> ?
```

### Retrieving All Characters
To get a combination of uppercase letters, lowercase letters, numbers, and special characters, use the all function:

```sh
all_chars = chars.all()
print(all_chars)
# Output: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~`!@#$%^&*()-_=+|[]\{|};':",./<>? 1234567890
```

You can install the package using `pip3`:

```sh
pip3 install chars
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.