import time
import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render
from django.views import generic
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, get_list_or_404, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet
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
    paginate_by = 10

    def get_queryset(self):
        # 重写通用视图的 get_queryset 函数，获取定制数据
        queryset = super(IndexView, self).get_queryset()

        # 日期归档
        year = self.kwargs.get('year', 0)
        month = self.kwargs.get('month', 0)

        # 标签
        tag = self.kwargs.get('tag', 0)

        # 导航条
        self.big_slug = self.kwargs.get('bigslug', '')

        # 文章分类
        slug = self.kwargs.get('slug', '')

        if self.big_slug:
            big = get_object_or_404(BigCategory, slug=self.big_slug)
            queryset = queryset.filter(category__bigcategory=big)

            if slug:
                slu = get_object_or_404(Category, slug=slug)
                queryset = queryset.filter(category=slu)

        if year and month:
            queryset = get_list_or_404(queryset, create_date__year=year, create_date__month=month)

        if tag:
            tags = get_object_or_404(Tag, name=tag)
            self.big_slug = BigCategory.objects.filter(category__article__tags=tags)
            self.big_slug = self.big_slug[0].slug
            queryset = queryset.filter(tags=tags)

        return queryset


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

    # template_name属性用于指定使用哪个模板进行渲染
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


@csrf_exempt
def LoveView(request):
    data_id = request.POST.get('um_id', '')
    if data_id:
        article = Article.objects.get(id=data_id)
        article.loves += 1
        article.save()
        return HttpResponse(article.loves)
    else:
        return HttpResponse('error', status=405)


class MySearchView(SearchView):
    # 返回搜索结果集
    context_object_name = 'search_list'
    # 设置分页
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    # 搜索结果以浏览量排序
    queryset = SearchQuerySet().order_by('-views')
