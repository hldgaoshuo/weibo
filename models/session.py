import time

from models.model_basic import Model
from utils import log, random_string


class Session(Model):
    """
    Session 是用来保存 session 的 model
    """

    def __init__(self, form):
        super().__init__(form)
        self.session_id = form.get('session_id', '')
        self.user_id = form.get('user_id', -1)
        self.expired_time = form.get('expired_time', time.time() + 3600)

    def expired(self):
        now = time.time()
        result = self.expired_time < now
        log('expired', result, self.expired_time, now)
        return result

    @classmethod
    def add(cls, user_id):
        session_id = random_string()
        form = dict(
            session_id=session_id,
            user_id=user_id,
        )
        s = Session.new(form)
        s.save()
        return session_id
