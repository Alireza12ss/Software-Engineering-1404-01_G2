from django.urls import path, re_path
from . import views

app_name = "team6"

urlpatterns = [
    # صفحه اصلی تیم 6 (لیست مقالات)
    path("", views.ArticleListView.as_view(), name="index"),
    
    # ویو پایه / API پایه
    path("ping/", views.ping, name="ping"),
    
    # اضافه کردن مقاله
    path("create/", views.ArticleCreateView.as_view(), name="article_add"),
    
    # جزئیات مقاله با slug
    re_path(r'^article/(?P<slug>[^/]+)/$', views.article_detail, name='article_detail'),
    
    # ویرایش مقاله
    re_path(r'^article/(?P<slug>[^/]+)/edit/$', views.edit_article, name="article_edit"),
    
    # نمایش نسخه‌ها
    re_path(r'^article/(?P<slug>[^/]+)/revisions/$', views.article_revisions, name="article_revisions"),
    
    # گزارش مقاله با slug (ساده‌ترین راه)
    re_path(r'^article/(?P<slug>[^/]+)/report/$', views.report_article, name="article_report"),
    
    # API خارجی برای محتوا
    path("api/wiki/content", views.get_wiki_content, name="external_api"),
]