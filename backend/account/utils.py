from django.db import transaction
import uuid


def get_current_session(request):
    session_obj = request.session.session_key
    return request.user.session_set.get(session_key=session_obj).get_decoded()


def set_new_session(request):
    session = request.session
    user = request.user
    uuid_str = str(uuid.uuid4())
    session["session_id"] = uuid_str
    session["customer"] = user.get_name()
    return uuid_str


def reset_user(request):
    user = request.user
    if user.is_authenticated:
        with transaction.atomic():
            user.first_name = ''
            user.save()
            seats = user.get_seats()
            for seat in seats:
                seat.seat_name = ''
                seat.save()
    else:
        return


def delete_all_sessions(request):
    user = request.user
    if user.is_authenticated:
        with transaction.atomic():
            user.session_set.all().delete
    return


def is_table_user(user):
    return user.groups.filter(name='Table').exists()


def is_manager_user(user):
    return user.groups.filter(name='Manager').exists()
