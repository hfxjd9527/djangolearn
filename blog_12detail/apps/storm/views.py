import time
import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render
from django.views import generic
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, BigCategory, Category, Tag


# Create your views here.
class IndexView(generic.ListView):
    """
        首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
    """
    # 获取数据库中的文章列表
    model = Article
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'index.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'articles'


def MessageView(request):
    return render(request, 'message.html', {'category': 'message'})


def AboutView(request):
    return render(request, 'about.html', {'category': 'about'})


def DonateView(request):
    return render(request, 'donate.html', {'category': 'donate'})


def ExchangeView(request):
    return render(request, 'exchange.html', {'category': 'exchange'})


class DetailView(generic.DetailView):
    """
        Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
    """
    # 获取数据库中的文章列表
    model = Article

    # template_name 属性用于指定使用哪个模板进行渲染
    template_name = 'article.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'article'

    def get_object(self):
        obj = super(DetailView, self).get_object()
        # 设置浏览量增加时间判断，同一篇文章两次浏览超过半小时才重新统计阅读量，作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if u != obj.author:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
        else:
            now_time = time.time()
            t = now_time - is_read_time
            if t > 60 * 30:
                obj.update_views()
                ses[the_key] = time.time()

        # 文章可以使用Markdown书写，带格式的文章，像CSDN写Markdown文章一样
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        obj.body = md.convert(obj.body)
        obj.toc = md.toc
        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['category'] = self.object.id
        return context
