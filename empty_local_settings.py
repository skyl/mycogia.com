SERVE_MEDIA = False

if SERVE_MEDIA:
    # bit leaky, but this is the one for 127.0.0.1:8000
    GOOGLE_API_KEY = 'ABQIAAAABH87p-yQOJj-sh06NusQiRTpH3CbXHjuCVmaTc5MkkU4wO1RRhTdrjDBgVDitkd2sidQwpIj12NE2w'
else:
    GOOGLE_API_KEY = 'ABQIAAAABH87p-yQOJj-sh06NusQiRSr0qcHqeiMmV61oMhjG2xscSbRchTwsY7jVmIrYL1h4TJCz-zrYddEPw'

BEHIND_PROXY = True

ADMINS = (
    ('Skylar Saveland', 'skylar.saveland@gmail.com'),
)

DEBUG = False
SERVE_MEDIA = False
DATABASE_NAME = 'mycogia'
DATABASE_USER = 'skyl'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'skylar.saveland@mycogia.com'
EMAIL_HOST_PASSWORD = 'tang53'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'skylar.saveland@mycogia.com'

DUMMY_FACEBOOK_INFO = {
    'uid':0,
    'name':'(Private)',
    'first_name':'(Private)',
    'pic_square_with_logo':'/public/images/t_silhouette.jpg',
    'affiliations':'server goof',
    'status':'facebook messed up',
    'proxied_email':None,
}
# mycogia.com
FACEBOOK_API_KEY = '36becd9314f8ce34ba2ebcdcb6d70f97'
FACEBOOK_SECRET_KEY = '06b05e75fa7f114cc27b5896b6578c24'

# local development
#FACEBOOK_API_KEY = 'dbee7c681fb8b3c375c5fc4fedea46e0'
#FACEBOOK_SECRET_KEY = 'b3f2adf023c9af70934c003e1c438d7c'
FACEBOOK_INTERNAL = True

BBAUTH_APP_ID = 'TgqJh0TIkY1_4ffM9xkwv4DOdJlUm5dqo5tnhEpVXg--'
BBAUTH_SHARED_SECRET = 'ae4729137e3f841dcf4375086ba117de'


MEDIA_URL = 'http://media.mycogia.com/'
ADMIN_MEDIA_PREFIX = 'http://media.mycogia.com/admin/'

SECRET_KEY = 'a&k4b8tkg0rgm44-!p^(wlx*9kzy6-4l@+%n@1izx(l*bq@kk*'


