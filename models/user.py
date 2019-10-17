import hashlib

from models.model_basic import Model
from models.user_role import UserRole


class User(Model):
    """
    User 是一个保存用户数据的 model
    """

    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', UserRole.normal)

    @staticmethod
    def guest():
        form = dict(
            id=-1,
            username='【游客】',
            role=UserRole.guest,
        )
        u = User(form)
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    @staticmethod
    def salted_password(password):
        salt = 'jdklajskldjkassapsqwekjsldasdasqwweq'
        salted = password + salt
        hashed = hashlib.sha256(salted.encode()).hexdigest()
        return hashed

    @classmethod
    def login_user(cls, form):
        username = form['username']
        salted = cls.salted_password(form['password'])
        u = User.find_by(username=username, password=salted)
        if u is None:
            result = '用户名或者密码错误'
        else:
            result = '登录成功'
        return u, result

    @classmethod
    def register_user(cls, form):
        u = User(form)
        valid = len(u.username) > 2 and len(u.password) > 2
        if valid:
            u.password = cls.salted_password(u.password)
            u.save()
            return '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            return '用户名或者密码长度必须大于2'
