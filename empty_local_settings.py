if SERVE_MEDIA:
    # this is the one for 127.0.0.1:8000
    GOOGLE_API_KEY = ''
else:
    GOOGLE_API_KEY = ''

BEHIND_PROXY = True

ADMINS = (
    ('you', 'you@gmail.com'),
)
SERVE_MEDIA = False

DEBUG = False
SERVE_MEDIA = False
DATABASE_NAME = ''
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with


EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''

DUMMY_FACEBOOK_INFO = {
    'uid':0,
    'name':'(Private)',
    'first_name':'(Private)',
    'pic_square_with_logo':'/public/images/t_silhouette.jpg',
    'affiliations':'server goof',
    'status':'facebook messed up',
    'proxied_email':None,
}
# domain.com
FACEBOOK_API_KEY = ''
FACEBOOK_SECRET_KEY = ''

# local development
#FACEBOOK_API_KEY = ''
#FACEBOOK_SECRET_KEY = ''
FACEBOOK_INTERNAL = True

BBAUTH_APP_ID = ''
BBAUTH_SHARED_SECRET = ''


MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = ''

SECRET_KEY = ''


