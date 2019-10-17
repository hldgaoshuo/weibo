from models.model_basic import Model


class Todo(Model):
    """
    针对数据 TODO 要做 4 件事情
    C create 创建数据
    R read 读取数据
    U update 更新数据
    D delete 删除数据
    """

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)

    @classmethod
    def add(cls, form, user_id):
        t = Todo.new(form)
        t.user_id = user_id
        t.save()

    @classmethod
    def update(cls, id, form):
        t = Todo.find_by(id=id)
        t.title = form['title']
        t.save()
