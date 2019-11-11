from django.conf import settings

from home.models import EmailMessageLog,EmailMessageType



class LinuxjobberMailer:
    def __init__(self,
                 subject:str,
                 message:str,
                 to_address:str,
                 header_text:str = "",
                 type:EmailMessageType = None
                 ):
        # self.subject = subject,
        # self.to_address = to_address,
        # self.header_text = header_text,
        # self.type = type,
        # self.content = message

        self.message_item = EmailMessageLog.objects.create(
            subject = subject,
            to_address = to_address,
            header_text =  header_text,
            message_type = type,
            content = message
        )

    def send_mail(self):
        send_mail_with_client(self.message_item)



def send_mail_with_client(message: EmailMessageLog):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    plaintext = get_template('home/email_template.txt')
    htmly = get_template('home/email_template.html')
    formatted_sender_name = message.header_text + " <{}>".format(settings.EMAIL_HOST_USER)

    context = {
        'sender_name': message.header_text,
        'subject':message.subject,
        'message': message.content
    }

    subject, from_email, to = message.subject, formatted_sender_name, message.to_address
    text_content = plaintext.render(context)
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
