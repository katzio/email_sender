#!/usr/bin/env python3
import os
from email_sender import get_gmail_service, create_message_with_template, send_message

def send_demo_email():
    """Send a demo email to yourself using the email template."""
    print("Sending a demo email to yourself...")
    
    # Get Gmail API service
    service = get_gmail_service()
    
    # Set sender as Aryeh Katz with default email
    sender = "Aryeh Katz <dxdarie@gmail.com>"
    
    # Your own email for testing
    recipient = "dxdarie@gmail.com"
    
    # Email subject
    subject = "SCE 2015 Drive - לינק לדרייב 2015"
    
    # Email template file
    template_file = "email_template.html"
    
    # Check if template exists
    if not os.path.exists(template_file):
        print(f"Error: Template file '{template_file}' not found.")
        return
    
    print(f"Creating email using template: {template_file}")
    print(f"From: {sender}")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    
    # Create the message
    message = create_message_with_template(sender, [recipient], subject, template_file)
    
    # Confirm before sending
    confirm = input("\nSend the demo email? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Send the message
    sent_message = send_message(service, message)
    
    if sent_message:
        print("Demo email sent successfully!")
    else:
        print("Failed to send demo email.")

if __name__ == '__main__':
    send_demo_email() 