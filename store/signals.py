from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static
from django.urls import reverse


@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:  # Only send email on user creation
        print(f"User created: {instance.first_name}")  # Debugging line
        subject = "Registration Successful"

        # Prepare the context for the template
        context = {
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "icon_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZVj-T08Y93KX4OTxjcN-GdI1cUxQwupNr1w&s",  # Use the static function
            "login_url": reverse(
                "login"
            ),  # Replace with your actual login URL
        }

        # Render the HTML email content
        html_message = render_to_string("registration_email.html", context)

        # Create the email
        email = EmailMultiAlternatives(
            subject,
            "This is a fallback message if the HTML is not rendered.",  # Plain text fallback
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
