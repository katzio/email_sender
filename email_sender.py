#!/usr/bin/env python3
import os
import base64
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Get an authorized Gmail API service instance."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def get_label_id(service, label_name='SCE'):
    """Get the ID of a specific label."""
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    
    label_id = None
    for label in labels:
        if label['name'] == label_name:
            label_id = label['id']
            break
    
    if not label_id:
        print(f"Label '{label_name}' not found.")
    
    return label_id

def get_emails_from_label(service, label_id):
    """Fetch all email addresses and message IDs from emails in a specific label."""
    if not label_id:
        return [], []
    
    # Get messages with this label
    results = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
    messages = results.get('messages', [])
    
    # Continue fetching if there are more messages (pagination)
    while 'nextPageToken' in results:
        page_token = results['nextPageToken']
        results = service.users().messages().list(
            userId='me', labelIds=[label_id], pageToken=page_token).execute()
        messages.extend(results.get('messages', []))
    
    email_addresses = []
    message_ids = []
    
    for message in messages:
        message_ids.append(message['id'])
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        
        # Extract headers
        headers = msg['payload']['headers']
        
        # Look for Reply-To header first
        reply_to_header = next((header for header in headers if header['name'] == 'Reply-To'), None)
        
        if reply_to_header:
            # Extract email from Reply-To header
            reply_to_value = reply_to_header['value']
            if '<' in reply_to_value and '>' in reply_to_value:
                email = reply_to_value[reply_to_value.find('<')+1:reply_to_value.find('>')]
                email_addresses.append(email)
            else:
                email_addresses.append(reply_to_value)
        else:
            # Fall back to From header if Reply-To is not present
            from_header = next((header for header in headers if header['name'] == 'From'), None)
            if from_header:
                # Extract email from "Name <email@example.com>" format
                from_value = from_header['value']
                if '<' in from_value and '>' in from_value:
                    email = from_value[from_value.find('<')+1:from_value.find('>')]
                    email_addresses.append(email)
                else:
                    email_addresses.append(from_value)  # Use as is if no angle brackets
    
    # Remove duplicates from email addresses but keep message IDs intact
    return list(set(email_addresses)), message_ids

def delete_messages(service, message_ids):
    """Delete messages by ID."""
    if not message_ids:
        return
    
    # Use batch delete to remove messages
    service.users().messages().batchDelete(
        userId='me', 
        body={'ids': message_ids}
    ).execute()
    
    print(f"Successfully deleted {len(message_ids)} messages.")

def create_message_with_template(sender, bcc_list, subject, template_file):
    """Create an email message with HTML template."""
    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['Subject'] = subject
    
    # Add BCC recipients
    if bcc_list:
        message['Bcc'] = ', '.join(bcc_list)
    
    # Read HTML template
    with open(template_file, 'r') as file:
        html_content = file.read()
    
    # Attach HTML part
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)
    
    # Convert message to base64 encoded format
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, message):
    """Send an email message."""
    try:
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        print(f"Message sent. Message ID: {sent_message['id']}")
        return sent_message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Get Gmail API service
    service = get_gmail_service()
    
    # Get label ID - always use SCE label
    label_name = "SCE"
    label_id = get_label_id(service, label_name)
    
    if not label_id:
        print(f"Label '{label_name}' not found. Exiting.")
        return
    
    # Get email addresses from label
    print(f"Fetching email addresses from '{label_name}' label...")
    email_addresses, message_ids = get_emails_from_label(service, label_id)
    print(f"Found {len(email_addresses)} unique email addresses from {len(message_ids)} emails.")
    
    # Print all fetched email addresses
    print("\nEmail addresses fetched:")
    for i, email in enumerate(email_addresses, 1):
        print(f"{i}. {email}")
    print()
    
    if not email_addresses:
        print("No email addresses found. Exiting.")
        return
    
    # Determine if this is a dry run
    dry_run = input("Preview only? (y = preview addresses, n = proceed to send emails): ").lower() == 'y'
    
    if dry_run:
        print("\nPREVIEW MODE - No emails will be sent or deleted.")
        return
    
    # Set sender as Aryeh Katz with default email
    sender = "Aryeh Katz <dxdarie@gmail.com>"
    subject = input("Enter email subject: ")
    template_file = input("Enter path to HTML template file (default: email_template.html): ") or "email_template.html"
    
    # Confirm before sending
    print(f"\nReady to send email to {len(email_addresses)} recipients (BCC).")
    confirm = input("Send the email? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Create and send the message
    message = create_message_with_template(sender, email_addresses, subject, template_file)
    sent_message = send_message(service, message)
    
    if sent_message:
        # Verify email was sent successfully
        print("Email sent successfully!")
        
        # Ask if user wants to delete original emails
        delete_confirm = input("Delete all emails under the label? (y/n): ")
        if delete_confirm.lower() == 'y':
            delete_messages(service, message_ids)
        else:
            print("Emails were not deleted.")
    else:
        print("Failed to send email. Original emails were not deleted.")

if __name__ == '__main__':
    main() 