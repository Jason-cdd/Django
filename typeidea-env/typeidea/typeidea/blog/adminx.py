from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry
from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager, RelatedFieldListFilter
import xadmin

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

# Register your models here.


class PostInline:
    form_layout = (
        Container(
            Row('title', 'desc'),
        )
    )
    extra = 1
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器只展示当前用户分类"""
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookuo_choices, 根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ['title', 'category', 'status',
                    'created_time', 'owner', 'operator']
    list_display_links = []

    list_filter = ['category', ]
    search_fields = ['title', 'category__name']

    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    exclude = ['owner']
    # fields = (('category', 'title'), 'desc', 'status', 'content', 'tag')
    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )
    filter_vertical = ('tag', )

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('xadmin:blog_post_change', args=(obj.id, )))
    operator.short_description = '操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # @property
    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )

