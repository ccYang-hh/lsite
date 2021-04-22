from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def jinja2_environment(**options):
    env = Environment(**options)
    # 向jinja2的全局环境变量中添加static、url两个django api
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env