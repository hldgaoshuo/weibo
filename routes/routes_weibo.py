from utils import log
from models.comment import Comment
from models.weibo import Weibo
from routes.routes_basic import (
    redirect,
    current_user,
    html_response,
    login_required,
)


def index(request):
    """
    weibo 首页的路由函数
    """
    u = current_user(request)
    ws = Weibo.find_all(user_id=u.id)
    return html_response('weibo_index.html', weibos=ws, user=u)


def add(request):
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    Weibo.add(form, u.id)
    return redirect('/weibo/index')


def delete(request):
    weibo_id = int(request.query['weibo_id'])
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query['weibo_id'])
    w = Weibo.find_by(id=weibo_id)
    return html_response('weibo_edit.html', weibo=w)


def update(request):
    """
    用于增加新 weibo 的路由函数
    """
    form = request.form()
    weibo_id = int(form['weibo_id'])
    Weibo.update(weibo_id, form['content'])
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    form = request.form()
    weibo_id = int(form['weibo_id'])

    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo_id
    c.save()

    log('comment add', c, u, form)
    return redirect('/weibo/index')


def weibo_owner_required(route_function):
    def f(request):
        log('weibo_owner_required')
        u = current_user(request)
        id_key = 'weibo_id'
        if id_key in request.query:
            weibo_id = request.query[id_key]
        else:
            weibo_id = request.form()[id_key]

        w = Weibo.find_by(id=int(weibo_id))
        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')
    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        # 微博
        '/weibo/index': login_required(index),
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        # 评论
        '/comment/add': login_required(comment_add),
    }
    return d
