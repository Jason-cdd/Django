# coding:utf-8

from .base import *  # NOQA

DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',   # 此处和文章不一样
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# INSTALLED_APPS += [
#     'debug_toolbar',
# ]
#
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

INTERNAL_IPS = ['127.0.0.1']

if DEBUG:
    # django debug toolbar
    INSTALLED_APPS.append('debug_toolbar')
    INSTALLED_APPS.append('pympler')
    INSTALLED_APPS.append('debug_toolbar_line_profiler')
    INSTALLED_APPS.append('silk')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
        # 或把jquery下载到本地然后取消下面这句的注释, 并把上面那句删除或注释掉
        #'JQUERY_URL': '/static/jquery/2.1.4/jquery.min.js',
        'SHOW_COLLAPSED': True,
        'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }


DEBUG_TOOLBAR_PANELS = [
    # 'djdt_flamegraph.FlamegraphPanel',
    # 'pympler.panels.MemoryPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
]
