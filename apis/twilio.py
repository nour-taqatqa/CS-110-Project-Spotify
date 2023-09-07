try:
    import authentication, utilities
    utilities.modify_system_path()
except:
    pass

from apis import authentication
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_mail(from_email:str, to_emails:list, subject:str, html_content:str):
    '''
    Uses the SendGrid API to send an email.  

    * from_email(str):          [Required] The sender's email.  
    * to_emails(list or str):   [Required] A list or of recipient emails, string is fine for one recipient.  
    * subject(str):             [Required] The subject of the email.   
    * html_content(str):        [Required] Text or HTML to be included in the body of the email.  
    
    Returns True if the email was successfully sent, False otherwise.
    '''
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )

    try:
        token = authentication.get_token('https://www.apitutor.org/sendgrid/key')
        sg = SendGridAPIClient(token)
        sg.send(message)
        print('Email sent. You may need to check your spam folder.')
        return True
    except Exception as e:
        print(e)
        return False
