from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class Emails:
    """Email class for sending emails."""
    def __init__(self, order=None, user=None, email=None, question=None, product_url=None, pk=None):
        self.order = order
        self.user = user
        self.email = email
        self.question = question
        self.product_url = product_url
        self.pk = pk
        self.mail_subject = None
        self.message = None
        self.redirect_to_function()

    def redirect_to_function(self):
        """Redirecting function."""
        if self.user is not None:
            if self.question is not None:
                self.question_email()

            elif self.order is not None:
                self.order_email()

            else:
                self.confirm_email()

        else:
            self.new_order_email()

    def question_email(self):
        """Sending email to admins if question."""
        self.mail_subject = 'Новый вопрос на сайте'
        self.message = render_to_string('accounts/question_email.html', {
            'name': self.user,
            'email': self.email,
            'question': self.question,
            'product_url': self.product_url,
        })
        self.send_email_to_admins()

    def new_order_email(self):
        """Sending email to admins if new order in a site."""
        self.mail_subject = 'Новый заказ на сайте'
        self.message = render_to_string('accounts/new_order.html', {'order_id': self.order})
        self.send_email_to_admins()

    def order_email(self):
        """Sending email to user after buying."""
        self.mail_subject = 'Спасибо за покупку!'
        self.message = render_to_string('orders/order_received_email.html', {'user': self.user, 'order': self.order})
        self.send_email_to_user()

    def confirm_email(self):
        """Sending email for user after registration."""
        self.mail_subject = 'Подтверждение почты'
        self.message = render_to_string('accounts/account_verification_email.html', {
            'user': self.user,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': default_token_generator.make_token(self.user),
            'email': self.email,
        })
        self.send_email_to_user()

    def send_email_to_admins(self):
        """Sending mass email to admins."""
        send_mass_mail = EmailMessage(self.mail_subject, self.message, to=[
            'mila-iris@mila-iris.kz',
            'anuar123@mail.ru',
            'botaonelove@yandex.ru',
            'anuar.umarov@gmail.com'])
        send_mass_mail.send()

    def send_email_to_user(self):
        """Sending email to user."""
        send_email = EmailMessage(self.mail_subject, self.message, to=[self.email])
        send_email.send()
