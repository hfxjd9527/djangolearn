from django.contrib import admin
from .models import Article, Tag, Category, Carousel, Keyword, FriendLink, BigCategory


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 这个的作用就是给一个筛选机制，一般按照时间比较好
    date_hierarchy = 'created_date'
    exclude = ('views',)
    list_display = ('id', 'title', 'author', 'created_date', 'updated_date')
    # 设置需要添加<a>标签的字段
    list_display_links = ('title',)
    # 筛选过滤器
    list_filter = ('created_date', 'category')
    list_per_page = 50  # 控制每页显示的对象数量，默认是100
    filter_horizontal = ('tags', 'keywords')  # 给多选增加一个左右添加的框

    # 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')


@admin.register(BigCategory)
class BigCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')


# 自定义管理站点的名称和URL标题
admin.site.site_header = '网站管理'
admin.site.site_title = '博客后台管理'


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'content', 'img_url', 'url')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'link', 'created_date', 'is_active', 'is_show')
    date_hierarchy = 'created_date'
    list_filter = ('is_active', 'is_show')
