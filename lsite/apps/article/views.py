from django.shortcuts import render,get_object_or_404
from django.utils.safestring import mark_safe
import markdown

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from article.models import Article
from article.serializers import ArticleSerializer


class ArticleView(APIView):

    def get(self, request, pk, format=None):
        article = get_object_or_404(Article,id=pk)
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                #'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        article.body = md.convert(article.body)
        article.body = mark_safe(article.body)
        serializer = ArticleSerializer(article, context={'request': request})
        context = {
            'article': serializer.data,
            'toc': md.toc
        }
        return Response(context)


class ArticlePagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 10
    page_size_query_param = 'page_size'


class ArticlesListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self):
        query_dict = self.request.query_params  # QueryDict类型，其api参考官网
        if not query_dict:
            return Article.objects.all()
        else:
            types = query_dict.getlist('type')  # getlist() api 用于获取某个查询参数的列表
            if not types:
                return Article.objects.all()
            else:
                articles = Article.objects.filter(tags__name__in=types)
                return articles
