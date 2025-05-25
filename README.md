# Gmail Mass Email Sender

A Python script for sending mass emails using the Gmail API, with all recipients added as BCC.

## Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd drive_autosender
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Google API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API for your project
   - Create OAuth 2.0 credentials
     - Application type: Desktop application
     - Download the credentials file and save it as `credentials.json` in the project directory

## Usage

1. Customize the HTML email template by editing `email_template.html` to fit your needs.

2. Run the script:
   ```
   python email_sender.py
   ```

3. The script will:
   - Authenticate with your Google account (first time will open a browser window)
   - Ask you for the label name to process (default is "SCE")
   - Fetch all email addresses from emails in the specified label
   - Ask if you want to run in dry mode (just show addresses without sending/deleting)
   - If not in dry mode:
     - Prompt you for your email address, subject, and template file
     - Send a mass email with all recipients in BCC
     - Verify the email was sent successfully
     - Optionally delete all emails under the label after confirmation

## Features

- **Dry Run Mode**: Test the script without sending emails or deleting anything
- **Email Template**: Customize the HTML template for your outgoing emails
- **BCC Recipients**: All recipients are added as BCC for privacy
- **Email Cleanup**: Option to delete source emails after successfully sending the mass email

## Notes

- When first running the script, you'll need to authorize it through your Google account.
- The token.json file is created after authentication and stores your credentials securely.
- If you modify the SCOPES in the script, delete token.json to re-authenticate.
- The script removes duplicate email addresses before sending. 

## Repository Integrity

For verification purposes in the email template, we use a hash that excludes both the template itself and this README (to avoid circular references):
```
d152f8d30f12c11f6a7c9dd718df71755e172d0947faec5d0d28e4a54690785f
```

Generate this non-circular hash with:
```
git ls-files | grep -v -e email_template.html -e README.md | xargs cat | shasum -a 256
``` 