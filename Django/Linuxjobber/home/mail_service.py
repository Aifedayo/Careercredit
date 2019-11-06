from django.conf import settings

from Django.Linuxjobber.home.models import EmailMessageLog




def send_mail_with_client(message: EmailMessageLog):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    plaintext = get_template('home/email.txt')
    htmly = get_template('home/email_template.html')
    sender_name = message.

    d = {
        'from_address': message.from_address,
        'sender_name': message.from_address,
        'senator_name': message.to_address,
        'message': message.content
    }

    subject, from_email, to = message.subject,"{} from Linuxjobber <{}>".format(
        message.sender_name,
        settings.EMAIL_HOST_USER), message.to_address
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
