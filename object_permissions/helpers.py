from django.core.exceptions import PermissionDenied


def has_permissions_or_403(user, maybe_iterable, obj):
    # maybe_iterable - jesli jest stringiem/unicodem - musi byc owrapowane w liste
    # (dla zachowania wspolnego interfejsu ponizej)
    if isinstance(maybe_iterable, basestring):
        maybe_iterable = [maybe_iterable]

    # user musi miec wszystkie wymienione uprawnienia
    for permission in maybe_iterable:
        if not user.has_perm(permission, obj):
            # TODO PermissionDenied uzyskane ta droga jest nienajladniejsze; w razie potrzeby mozna:
            # http://stackoverflow.com/questions/2299077/creating-custom-exceptions-that-django-reacts-to
            raise PermissionDenied()
