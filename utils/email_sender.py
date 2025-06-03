import smtplib
from email.message import EmailMessage

def send_email_with_attachments(PDF_REPORT, CHECKLIST_PDF):
    msg = EmailMessage()
    msg['Subject'] = 'Walk Tracker Report'
    msg['From'] = ''
    msg['To'] = ['']

    msg.set_content("Please find attached:\n- Checklist Responses (PDF)\n- Walk Route Map (PDF)")

    with open(CHECKLIST_PDF, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='Checklist.pdf')

    with open(PDF_REPORT, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='WalkMap.pdf')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('sender mail', 'App password')  # App password
        smtp.send_message(msg)


