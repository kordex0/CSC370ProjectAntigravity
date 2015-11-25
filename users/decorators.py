
from users.models import User

def get_request_user(func):
    def inner(request, *args, **kwargs):
        try:
            user = request.user.user
        except (User.DoesNotExist, AttributeError):
            user = None
        return func(request, user, *args, **kwargs);
    return inner

