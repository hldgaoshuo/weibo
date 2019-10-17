from models.user import User


def test():
    with open(User.db_path(), 'w') as f:
        f.write('[]')

    form = dict(
        username='guagua',
        password='123',
    )
    User.register_user(form)

    u, result = User.login_user(form)
    assert u is not None


if __name__ == '__main__':
    test()
