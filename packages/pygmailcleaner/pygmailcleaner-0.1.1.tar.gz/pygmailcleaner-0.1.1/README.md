# PyGmailCleaner

PyGmailCleaner is a command-line interface (CLI) application designed to help you manage and clean up your Gmail inbox efficiently. It provides simple options to filter emails by various criteria and automate the deletion process.

## Features

- Filter emails by date, promotions, unread status, importance, and attachments.
- Interactive prompts for easy configuration.
- Option to delete emails immediately or after confirmation.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)
- Gmail account
- App password (if using 2-factor authentication)

## Installation

PyGmailCleaner can be installed using Poetry or pip from PyPI.

### Using Poetry

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Add PyGmailCleaner**:
   ```bash
   poetry add pygmailcleaner
   ```

3. **Install dependencies**:
   ```bash
   poetry install
   ```

### Using pip from PyPI

1. **Install PyGmailCleaner**:
   ```bash
   pip install pygmailcleaner
   ```

## Usage

Run the application using the following command:
```bash
pygmailcleaner --loglevel debug
```

### Command-Line Arguments

- `--loglevel`: Set the logging level (e.g., `debug`, `info`, `warning`, `error`). Default is `notset`.

### Interactive Prompts

The application will guide you through several prompts to configure the cleaning process:

1. **Email Credentials**: Enter your Gmail address and password if not set via environment variables. The password expected is an "app password" if your gmail uses two-factor which can be configured via: https://support.google.com/mail/answer/185833?hl=en-GB. 

2. **General Statistics**: The application will display the total number of messages and unread messages.

3. **Filter Date**: Specify a date to filter emails up until.

4. **Filter Selection**: Choose the filters to apply for identifying emails to be cleaned.

5. **Delete Immediately**: Choose whether to delete emails immediately or wait for confirmation.

6. **Summary**: Review your choices and confirm to proceed.
 
7. **Continue Confirmation**: Confirm whether to proceed with the deletion.

### Example Run

```plaintext
____ ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ ____ 
||P |||Y |||G |||M |||A |||I |||L |||       |||C |||L |||E |||A |||N |||E |||R ||
||__|||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\| 
        
Welcome to the Gmail Cleaner CLI
*******************************
What is your gmail address?: rupertarup@gmail.com
What is your password? (must be an app password if using 2FA): 
Connected to gmail
Total number of messages: 22614
Unread messages: 4714
What date would you like to clean up until? (format 'YYYY-MM-DD'): 2024-03-31
Please select the commands you would like to include:
Only include promotions? [y/n]: y
Only include unread? [y/n]: y
Exclude important? [y/n]: y
Exclude attachments? [y/n]: y
Would you like to delete immediately? [y/n]: y

Summary:
1. Search up until date: 2024-03-31
2. Delete immediately: Yes
3. Included filters:
   - Only include promotions
   - Only include unread
   - Exclude important
   - Exclude attachments
Would you like to continue? [y/n]: y
Moving 259 to Trash
Emptying Trash
Connection closed
Thank you for using the Gmail Cleaner CLI. Goodbye!
```

## Logging

Logs are printed to the console based on the specified log level. Available levels are `debug`, `info`, `warning`, `error`, and `notset`.

## Next steps

- Break the app into commands:
   - Delete by filters worflow (current)
   - Delete by top spammers workflow
   - Delete by specific email address
   - Delete by specific subject title

- Add more information to messages staged for deletion

What this app will not do:
   - Unsubscribe 


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact [ruperarup@gmail.com].

Thank you for using PyGmailCleaner!