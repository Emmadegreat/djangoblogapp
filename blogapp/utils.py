from django.core.mail import send_mass_mail
from .models import NewsLetter

def send_newsletter(subject, message):
    subscribers = NewsLetter.objects.filter(subscribed=True)
    recipient_list = [subscriber.email for subscriber in subscribers]

    if not recipient_list:
        return "No subscribers to send mail"

    messages =[
        (subject, message, 'emf0046@gmail.com', [email])
        for email in recipient_list
    ]
    send_mass_mail(messages, fail_silently=False)
    return f"Newsletter sent to{len(recipient_list)} subscribers"