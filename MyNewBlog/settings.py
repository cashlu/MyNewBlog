"""
Django settings for MyNewBlog project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qa8)*-gxdmo+yt=s_^jo%^#nr0ky_$_dc@*)-m)&c)p0v^e9*b'

# SECURITY WARNING: don't run with debug turned on in production!

# 生产环境下应该关闭debug，在allowed_hosts中添加可用来访问的域名或IP
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'comments.apps.CommentsConfig',
    'gunicorn',
    'haystack',
    'django_forms_bootstrap',
]
# 注册四个apps，blog，comments,gunicorn，haystack这里需要注意两点：
# 1、blog应用是在IDE创建项目的时候指定的，所以这里自动注册好了，其他的是在后来
#       手工添加的，所以需要自己手工注册一下。
# 2、注册的格式是[appName].apps.[appName]Config的格式(这个类在App目录下
#       的apps.py中定义的。)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyNewBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MyNewBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# 全文检索的配置信息
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# HAYSTACK_CONNECTIONS 的 ENGINE 指定了 django haystack 使用的搜索引擎，这里我们使用
# 了 blog.whoosh_cn_backend.WhooshEngine，虽然目前这个引擎还不存在，但我们接下来会创建
# 它。PATH 指定了索引文件需要存放的位置，我们设置为项目根目录 BASE_DIR 下的
# whoosh_index 文件夹（在建立索引是会自动创建）。
# HAYSTACK_SEARCH_RESULTS_PER_PAGE 指定如何对搜索结果分页，这里设置为每 10 项结果为一页。
# HAYSTACK_SIGNAL_PROCESSOR 指定什么时候更新索引，
# 这里我们使用 haystack.signals.RealtimeSignalProcessor，作用是每当有文章更新时就更新
# 索引。由于博客文章更新不会太频繁，因此实时更新没有问题。

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 全文检索的配置信息
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# HAYSTACK_CONNECTIONS 的 ENGINE 指定了 django haystack 使用的搜索引擎，这里我们使用
# 了 blog.whoosh_cn_backend.WhooshEngine，虽然目前这个引擎还不存在，但我们接下来会创建
# 它。PATH 指定了索引文件需要存放的位置，我们设置为项目根目录 BASE_DIR 下的
# whoosh_index 文件夹（在建立索引是会自动创建）。
# HAYSTACK_SEARCH_RESULTS_PER_PAGE 指定如何对搜索结果分页，这里设置为每 10 项结果为一页。
# HAYSTACK_SIGNAL_PROCESSOR 指定什么时候更新索引，
# 这里我们使用 haystack.signals.RealtimeSignalProcessor，作用是每当有文章更新时就更新
# 索引。由于博客文章更新不会太频繁，因此实时更新没有问题。