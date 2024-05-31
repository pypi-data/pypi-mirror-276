from django.contrib.auth import get_user_model
from social_core.exceptions import AuthAlreadyAssociated, AuthForbidden

User = get_user_model()


def _user_lookup(username):
    return {
        User.USERNAME_FIELD: username,
    }


def social_user(backend, uid, user=None, *args, **kwargs):
    user_kwargs = _user_lookup(kwargs["details"]["username"])
    user_qs = User.objects.filter(**user_kwargs)
    backend_allows_new_users = getattr(backend, "allow_new_users", False)

    if user_qs.exists():
        user = user_qs.first()
    elif backend_allows_new_users:
        user = User(**user_kwargs)
        user.set_unusable_password()
        user.save()
    else:
        raise AuthForbidden(backend)

    user = user_qs.first()

    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)

    if social:
        if user and social.user != user:
            msg = "Cannot associated federated with system user."
            raise AuthAlreadyAssociated(backend, msg)
        elif not user:
            user = social.user

    return {
        "social": social,
        "user": user,
        "is_new": user is None,
        "new_association": social is None,
    }
