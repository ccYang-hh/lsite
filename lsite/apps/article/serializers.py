from rest_framework import serializers

from article.models import Article
from taggit.models import TaggedItem
from taggit.managers import TaggableManager


class TagSerializerField(serializers.Field):
    """
    自定义TagSerializer字段
    """
    def __init__(self, **kwargs):
        # 默认只读
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, data):
        return ','.join(data.values_list('name', flat=True))

    def to_internal_value(self, data):
        return None


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """
    article的序列化器
    """
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Article
        # 尽量不要用__all__来指定fields，因为一旦模型被更改，可能会导致数据泄露
        fields = ['url', 'id', 'title', 'body', 'avatar', 'created',
                  'updated', 'total_views', 'tags', 'supports', 'isPrivate']
        extra_kwargs = {
            'url': {
                'view_name': 'article-detail'
            }
        }

    def get_tags(self, article):
        tag_list = []
        for tag in article.tags.all():
            tag_list.append(tag.name)
        return tag_list