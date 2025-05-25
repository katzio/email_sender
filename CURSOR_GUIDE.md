# Creating the Email Sender Project with Cursor

This guide will help beginners in computer engineering recreate this email sender project from scratch using [Cursor](https://cursor.sh), an AI-powered code editor.

## What is Cursor?

Cursor is a code editor based on VSCode that integrates powerful AI capabilities to help you write, understand, and modify code. It's particularly useful for beginners as it can:

- Generate code based on natural language descriptions
- Explain existing code in plain language
- Help debug and fix issues
- Suggest improvements to your code

## Prerequisites

Before starting, make sure you have:

1. [Cursor](https://cursor.sh) installed on your computer
2. Python 3.6 or higher installed
3. Basic understanding of Python programming
4. A Google account to use the Gmail API

## Step 1: Setting Up Your Project

1. Open Cursor and create a new folder for your project
2. In Cursor, create a new terminal and navigate to your project folder
3. Ask Cursor to help you set up a new Python project:

```
Create a new Python project for sending mass emails using Gmail API
```

## Step 2: Setting Up Google API Credentials

1. Visit the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API for your project
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials file and save it as `credentials.json` in your project directory

## Step 3: Creating the Email Sender Script

Ask Cursor to generate the main script by describing what you want:

```
Create a Python script that uses the Gmail API to:
1. Authenticate with a Google account
2. Fetch email addresses from emails in a specific Gmail label (SCE)
3. Send a mass email to all these addresses as BCC
4. Use an HTML template for the email content
5. Optionally delete the original emails after sending
```

Cursor will generate a script similar to `email_sender.py` in this project.

The script offers a streamlined workflow:

1. **Preview Mode**: Choose whether to just view the email addresses or proceed with actions
2. **Action Selection**: Choose from a menu of options:
   - Send emails and delete originals
   - Send emails without deleting originals
   - Delete originals without sending emails
3. **Confirmation**: Confirm before any sending or deletion occurs
4. **Execution**: Perform the selected action with appropriate feedback

The script handles error conditions gracefully, with fallbacks for operations that might fail due to permission issues.

## Step 4: Creating the Email Template

Ask Cursor to create an HTML email template:

```
Create an HTML email template with:
1. A heading
2. Some paragraphs of text
3. A button that links to a URL
4. A footer with attribution
Make sure it's properly formatted for HTML emails with right-to-left support for Hebrew text
```

Modify the template to suit your needs. Our template includes:

- Right-to-left text alignment for Hebrew
- A prominent button linking to a Google Drive
- Attribution in the footer with links to this project

## Step 5: Testing Your Script

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python email_sender.py
   ```

3. Follow the prompts to:
   - Choose preview mode or action mode
   - Review the email addresses found
   - Select what action to take (send, delete, or both)
   - Confirm your choices

The script uses proper Gmail API scopes to ensure all operations are authorized:
```python
SCOPES = [
    'https://mail.google.com/',  # Full access to Gmail account
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.compose'
]
```

## Step 6: Creating a Demo Script

If you want to test your email template without affecting multiple recipients or labeled emails:

```
Create a script that sends a test email to myself using the template
```

Cursor will generate a script like `send_demo_email.py` in this project. This is useful for:
- Previewing how your email will look
- Testing the template before sending to multiple recipients
- Verifying authentication works correctly

## Tips for Working with Cursor

1. **Be specific in your requests**: The more details you provide, the better Cursor can help you.

2. **Iterate with follow-up questions**: If Cursor's output isn't quite right, ask for specific changes:
   ```
   Update the email template to align text to the right for RTL languages
   ```

3. **Ask for explanations**: If you don't understand something, ask:
   ```
   Explain how the authentication process works in this script
   ```

4. **Request improvements**: Ask Cursor to improve your code:
   ```
   Make the script more user-friendly by adding better prompts and error handling
   ```

## Common Issues and Solutions

If you encounter errors, ask Cursor for help:

```
I'm getting an authentication error when running the script. How do I fix it?
```

Or:

```
The email template doesn't display correctly in Gmail. How can I improve it?
```

## Next Steps

Once you've successfully recreated this project, you can ask Cursor to help you extend it:

- Add email tracking features
- Implement email scheduling
- Create a web interface for the email sender
- Add support for email attachments

## Conclusion

This project demonstrates how powerful AI-assisted coding can be, especially for beginners. Cursor makes it possible to create functional applications with minimal coding experience, allowing you to focus on understanding the concepts rather than getting stuck on syntax details.

Remember that AI is a tool to assist your learning, not replace it. Take time to understand the code that Cursor generates for you, and you'll build your programming skills much faster. 