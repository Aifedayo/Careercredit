import smtplib
import threading

from background_task import background
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.message import sanitize_address
from django.db.models import QuerySet



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import  logging
from home.models import EmailMessageLog, EmailGroupMessageLog

standard_logger = logging.getLogger(__name__)
class EmailThread(threading.Thread):
    def __init__(self, mass_mailer):
        threading.Thread.__init__(self)
        self.mailer = mass_mailer
        self.daemon = True
        self.start()

    def run(self):
        self.mailer.trigger_mail()
        standard_logger.info('Thread ended')

class CustomMailAlternative(EmailMultiAlternatives):

    def __init__(self,*args,**kwargs):
        super().__init__(*args)
        self.message_obj = None
        if 'message_obj' in kwargs:
            self.message_obj = kwargs['message_obj']

class CustomEmailBackend(EmailBackend):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)


    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        recipients = [sanitize_address(addr, encoding) for addr in email_message.recipients()]
        message = email_message.message()
        try:
            self.connection.sendmail(from_email, recipients, message.as_bytes(linesep='\r\n'))
            email_message.message_obj.set_as_sent()
        except smtplib.SMTPException as e:
            email_message.message_obj.set_as_fail(e)
            if not self.fail_silently:
                raise
            return False
        return True


    def send_messages(self,email_messages,total=0):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        # if not email_messages:
        #     return
        with self._lock:
            new_conn_created = self.open()
            if not self.connection or new_conn_created is None:
                # We failed silently on open().
                # Trying to send would be pointless.
                return
            num_sent = 0
            index = 0
            for message in email_messages:
                index+=1
                sent = self._send(message)
                if sent:
                    num_sent += 1
                # Sets group message log to completed
                if index == total and message.message_obj.group_log:
                    message.message_obj.group_log.set_as_completed()

            if new_conn_created:
                self.close()
        return num_sent

class LinuxjobberMailer:

    def __init__(self,
                 subject:str,
                 message:str,
                 to_address:str,
                 header_text:str = "",
                 type = None,
                 group_id:int = None
                 ):
        # self.subject = subject,
        # self.to_address = to_address,
        # self.header_text = header_text,
        # self.type = type,
        # self.content = message

        try:
            group_log = EmailGroupMessageLog.objects.get(pk=group_id)
        except:
            group_log = None



        self.message_item = EmailMessageLog.objects.create(
            subject = subject,
            to_address = to_address,
            header_text =  header_text,
            message_type = type,
            content = message,
            group_log = group_log
        )

    def send_mail(self):
        # if not self.message_item.header_text:
        #
        #
        # if self.message_item.message_type:
        #     self.message_item.header_text = self.message_item.message_type.header_format.format(
        #         self.message_item.header_text
        #     )

        self.message_item.send_mail()

class LinuxjobberMassMailer:
    def __init__(self, linuxjobber_mailer_list, is_queryset=False):
        if is_queryset:
            messages = linuxjobber_mailer_list
            self.total_messages = messages.count()
        else:
            messages = [mail.message_item for mail in linuxjobber_mailer_list]
            self.total_messages = len(messages)
        self.messages = list(map(generate_message,messages))


    def send(self):
        thread = EmailThread(self)

    def trigger_mail(self):
        from django.core import mail
        connection = mail.get_connection()
        # Manually open the connection
        connection.open()
        # Send the all the  emails in a single call -
        count = connection.send_messages(self.messages,self.total_messages)
        # The connection was already open so send_messages() doesn't close it.
        # We need to manually close the connection.
        connection.close()

@background(schedule=1)
def handle_campaign(group_id):
    from .models import  EmailGroupMessageLog
    message_template = EmailGroupMessageLog.objects.get(id=group_id)
    members = message_template.group.get_members_emails()
    transformed_members = [LinuxjobberMailer(
        subject= message_template.message.title,
        to_address= email,
        header_text="",
        type=None,
        group_id = group_id,
        message=message_template.message.message
    ) for email in members ]
    mailer = LinuxjobberMassMailer(transformed_members)
    mailer.send()


@background(schedule=1)
def handle_failed_campaign(group_id):
    try:
        group = EmailGroupMessageLog.objects.get(pk=group_id)
    except:
        return
    failed_messages = group.get_failed_messages()
    mailer = LinuxjobberMassMailer(failed_messages,is_queryset=True)
    mailer.send()



def generate_message(message):
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
    msg = CustomMailAlternative(subject, text_content, from_email, [to],message_obj=message)
    msg.attach_alternative(html_content, "text/html")
    return msg


def send_mail_with_client(message):
    message = generate_message(message)
    message.send()



if __name__ == '__main__':
    print('Done')