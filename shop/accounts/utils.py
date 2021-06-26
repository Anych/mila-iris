from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def email(order=None, user=None, mail=None, question=None, product_url=None):

    if user is not None:
        if question is not None:
            mail_subject = 'Новый вопрос на сайте'
            message = render_to_string('accounts/question_email.html', {
                'name': user,
                'email': email,
                'question': question,
                'product_url': product_url,
            })
            send_email_to_admins(mail_subject, message)
        else:
            mail_subject = 'Спасибо за покупку!'
            message = render_to_string('orders/order_received_email.html', {'user': user, 'order': order})
            send_email = EmailMessage(mail_subject, message, to=[mail])
            send_email.send()
    else:
        mail_subject = 'Новый заказ на сайте'
        message = render_to_string('accounts/new_order.html', {'order_id': order})
        send_email_to_admins(mail_subject, message)


def send_email_to_admins(mail_subject, message):
    send_mass_mail = EmailMessage(mail_subject, message, to=[
        'mila-iris@mila-iris.kz',
        'anuar123@mail.ru',
        'botaonelove@yandex.ru',
        'anuar.umarov@gmail.com'])
    send_mass_mail.send()
