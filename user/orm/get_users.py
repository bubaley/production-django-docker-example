from user.models import User


def get_active_users():
    return User.objects.filter(is_active=True)
