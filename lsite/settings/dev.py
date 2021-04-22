"""
Django settings for lsite project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os,sys
import jinja2
import django_redis
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--e#%771@ddgg2(w^a0sp-hd-$hpru-g_=bb510kli$=*@pvw1!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',  # 跨域
    'taggit',  # 标签

    'article.apps.ArticleConfig',
]

MIDDLEWARE = [
    # 插入CorsMiddleware到中间件列表，位置不能错
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'environment': 'lsite.jinja2_settings.jinja2_env.jinja2_environment'
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'lsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lsite',
        'USER': 'yl',
        'PASSWORD': 'Yl0727..',
        #'HOST': '192.168.43.184',
        'HOST': '192.168.31.172',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/dist/')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 日志系统配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {                     # 日志信息显示的格式
        'verbose': {
            'format': '[ %(asctime)s ] [ %(levelname)s ] %(module)s %(lineno)d : %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[ %(asctime)s ] %(module)s %(lineno)d : %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true':{  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {        # 日志处理方法
        'console': {     # 向终端输出日志
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'file': {        # 向文件输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR.parent, 'logs/lsite.log'),
            'filters': ['require_debug_true'],
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {         # 日志器，日志系统入口
        'django': {      # 定义一个叫做django的日志器
            'handlers': ['console', 'file'],  # 该日志器有两个handler，可以同时向终端与文件输出日志（多线程）
            'propagate': True,    # 是否继续向下层传递日志消息
            'level': 'INFO',      # 日志器接受的最低日志级别
        }
    },
}

# DRF配置项
REST_FRAMEWORK = {
    # 异常处理，使用我们自定义的异常处理
    'EXCEPTION_HANDLER': 'lsite.utils.exceptions.exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# 配置redis缓存
CACHES = {
     'default': {
         'BACKEND': 'django_redis.cache.RedisCache',
         # 如果redis在其它主机，这里需要将host更改为该主机ip
         'LOCATION': 'redis://192.168.31.172:6379/0',
         "OPTIONS": {
             "CLIENT_CLASS": "django_redis.client.DefaultClient",
         }
     },
     'session': {
         'BACKEND': 'django_redis.cache.RedisCache',
         'LOCATION': 'redis://192.168.31.172:6379/1',
         "OPTIONS": {
             "CLIENT_CLASS": "django_redis.client.DefaultClient",
         }
    },
     'verify_codes': {
         'BACKEND': 'django_redis.cache.RedisCache',
         'LOCATION': 'redis://192.168.31.172:6379/2',
         "OPTIONS": {
             "CLIENT_CLASS": "django_redis.client.DefaultClient",
         }
     }
}

# 配置session引擎 ：基于缓存的session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 配置session使用缓存的哪一个配置：使用default配置，即使用redis的1号数据库
SESSION_CACHE_ALIAS = "session"

# 允许所有来源访问本站资源
CORS_ORIGIN_ALLOW_ALL = True
# 跨域访问白名单
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8081',
    'http://localhost:8081',
    'http://192.168.31.147:8081',
]
# 跨域时允许携带cookie
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
