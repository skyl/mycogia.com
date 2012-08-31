import os

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.conf import settings

from django_openid.models import UserOpenidAssociation

try:
    any
except NameError:
    def any(seq):
        for x in seq:
            if x:
                return True
        return False

register = template.Library()

def openid_icon(openid, user):
    oid = u'%s' % openid
    matches = [u.openid == oid for u in UserOpenidAssociation.objects.filter(user=user)]
    if any(matches):
        return mark_safe(u'<img src="%s" alt="%s" />' % (
            os.path.join(settings.MEDIA_URL, 'images', 'openid-icon.png'),
            ugettext('Logged in with OpenID')
        ))
    else:
        return u''
register.simple_tag(openid_icon)
