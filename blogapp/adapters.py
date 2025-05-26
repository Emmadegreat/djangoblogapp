from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        email = request.session.get('socialaccount_sociallogin', {}).get('email')
        if email and User.objects.filter(email=email).exists():
            return False
        return True

    def populate_user(self, request, user, form):
        """
        Override to not set username since we don't use it
        """
        user.email = form.cleaned_data.get('email', '')
        user.first_name = form.cleaned_data.get('first_name', '')
        user.last_name = form.cleaned_data.get('last_name', '')
        return user


class NoUsernameSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        Populate user instance with data from social account without username
        """
        user = sociallogin.user
        user.email = data.get('email', '')
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Override the save_user method to avoid using username
        """
        user = sociallogin.user

        # Set email as primary identifier
        if not user.email:
            if hasattr(sociallogin, 'email_addresses'):
                email = sociallogin.email_addresses[0]
                user.email = email
            else:
                # If we can't get an email, we can't continue
                return None

        # Check if a user with this email already exists
        try:
            existing_user = User.objects.get(email=user.email)
            # Connect the social account to the existing user
            sociallogin.connect(request, existing_user)
            return existing_user
        except User.DoesNotExist:
            # Ensure the user doesn't already exist
            if not user.pk:
                user.save()

        return user