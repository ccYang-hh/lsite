from django.urls import path
from article.views import ArticleView,ArticlesListView

from rest_framework.urlpatterns import format_suffix_patterns

app_label = 'article'

urlpatterns = [
    path('articles/<int:pk>/', ArticleView.as_view(), name='article-detail'),
    path('articles/',ArticlesListView.as_view(), name='article-list')
]

urlpatterns = format_suffix_patterns(urlpatterns)