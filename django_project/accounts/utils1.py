from django.contrib.auth import get_user_model


def add_first_users():
    print('sadfgsdfgsdf')
    get_user_model().objects.create(first_name="Владимир", last_name="Иванов", password="asdfsadfds",
                                    email='tsdsd@mail.com', is_verified=True, phone=23423423, birthday='2000-02-02')
    get_user_model().objects.create(first_name="Сергей", last_name="Кузнецов", password="asdfsadfds",
                                    email='tsdssdd@mail.com', is_verified=True, phone=22421423, birthday='2000-08-05')
    get_user_model().objects.create(first_name="Иван", last_name="Сергеев", password="asdfsadfds",
                                    email='tsdswerd@mail.com', is_verified=True, phone=2312323423,
                                    birthday='2000-09-09')
    get_user_model().objects.create(first_name="Дмитрий", last_name="Афанасьев", password="asdfsadfds",
                                    email='tsbdsdfdsd@mail.com', is_verified=True, phone=231223423,
                                    birthday='1994-07-03')
    get_user_model().objects.create(first_name="Лев", last_name="Акользин", password="asdfsadfds",
                                    email='tsdssdfcvd@mail.com', is_verified=True, phone=212423423,
                                    birthday='2001-05-06')
