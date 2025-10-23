"""
Django settings for site1 project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# ⚙️ CÀI ĐẶT CƠ BẢN
# ============================================================

SECRET_KEY = 'django-insecure-ru6mqif+@^4z(xf_q7y(!6fcwo4r#0j)l72i^jy(8m_mincpsz'
DEBUG = True
ALLOWED_HOSTS = []

# ============================================================
# 🧱 CÁC ỨNG DỤNG ĐANG DÙNG
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps của bạn
    'home',  # <- có chứa trang đăng ký, đăng nhập
]

# ============================================================
# 🌐 MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'site1.urls'

# ============================================================
# 🧩 TEMPLATE
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Dùng thư mục templates ở ngoài cùng (nếu có)
        'DIRS': [BASE_DIR / 'templates'],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'site1.wsgi.application'

# ============================================================
# 💾 DATABASE
# ============================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================================
# 🔐 XÁC THỰC NGƯỜI DÙNG
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# 🌏 NGÔN NGỮ & MÚI GIỜ
# ============================================================

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# ============================================================
# 🖼️ MEDIA (HÌNH ẢNH NGƯỜI DÙNG UPLOAD)
# ============================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# 🎨 STATIC FILES (CSS, JS, IMAGES)
# ============================================================

STATIC_URL = '/static/'

# Django sẽ tìm file tĩnh ở 2 nơi:
STATICFILES_DIRS = [
    BASE_DIR / "static",         # static ngoài cùng
    BASE_DIR / "home" / "static" # static trong app home (nếu có)
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============================================================
# 🚪 LOGIN / LOGOUT
# ============================================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# ============================================================
# 🪪 MẶC ĐỊNH
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
