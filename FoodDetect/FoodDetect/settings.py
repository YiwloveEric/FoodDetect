"""
Django settings for FoodDetect project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0detn^y(ko@e%3hmru2dihs4@ayl!a2vt^jx0vjz3al=#!*=pr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'User',
    'Ingredient',
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FoodDetect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'FoodDetect.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "FoodDetect",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "123456",
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 指定文件上传的路径
MEDIA_ROOT = BASE_DIR / 'file/image'
# 指定文件的url路径


# 微信的appid
APPID = "wx83139b5b5deb646d"
# 微信的secret
SECRET = "fdbbf522578bc05cba7d9846de99bf08"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器，返回json数据
        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览器API渲染器，返回调试界面
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'User.authentication.UserAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (

        'rest_framework.parsers.JSONParser',

    ),
}

# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    # 参数名 类型 是否必须 说明
    # username str 是 用户名
    # password str 是 密码
    # 更多配置：https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
    # 3、登录接口开发
    # 1. 业务说明
    # 验证用户名和密码，验证成功后，为用户签发JWT，前端将签发的JWT保存下来。
    # 2. 后端接口设计
    # 请求方式： POST /login/
    # 请求参数： JSON 或 表单
    # 返回数据： JSON
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),  # 访问令牌的有效时间
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 刷新令牌的有效时间
    "ROTATE_REFRESH_TOKENS": False,  # 若为True，则刷新后新的refresh_token有更新的有效时间
    "BLACKLIST_AFTER_ROTATION": True,  # 若为True，刷新后的token将添加到黑名单中,
    "ALGORITHM": "HS256",  # 对称算法：HS256 HS384 HS512 非对称算法：RSA
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,  # if signing_key, verifying_key will be ignore.
    "AUDIENCE": None,
    "ISSUER": None,
    'USER_AUTHENTICATION_RULE':
        'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    "AUTH_HEADER_TYPES": ("Bearer",),  # Authorization: Bearer <token>
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",  # if HTTP_X_ACCESS_TOKEN,X_ACCESS_TOKEN: Bearer <token>
    "USER_ID_FIELD": "id",  # 使用唯一不变的数据库字段,将包含在生成的令牌中以标识用户
    "USER_ID_CLAIM": "user_id",
}

CACHES = {
    # default 是缓存名，可以配置多个缓存
    "default": {
        # 应用 django-redis 库的 RedisCache 缓存类
        "BACKEND": "django_redis.cache.RedisCache",
        # 配置正确的 ip和port
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            # redis客户端类
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # redis连接池的关键字参数
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100
            }
            # 如果 redis 设置了密码，那么这里需要设置对应的密码，如果redis没有设置密码，那么这里也不设置
            # "PASSWORD": "123456",
        }
    }
}