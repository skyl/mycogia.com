from datetime import datetime

from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.models import Tag

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

try:
    markup_choices = settings.WIKI_MARKUP_CHOICES  # reuse this for now; taken from wiki
except AttributeError:
    markup_choices = (
        ('rst', _(u'reStructuredText')),
        ('txl', _(u'Textile')),
        ('mrk', _(u'Markdown')),
    )

class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title           = models.CharField(_('title'), max_length=200)
    slug            = models.SlugField(_('slug'), max_length=200)
    author          = models.ForeignKey(User, related_name="added_posts")
    creator_ip      = models.IPAddressField(_("IP Address of the Post Creator"), blank=True, null=True)
    body            = models.TextField(_('body'))
    tease           = models.TextField(_('tease'), blank=True)
    status          = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments  = models.BooleanField(_('allow comments'), default=True)
    publish         = models.DateTimeField(_('publish'), default=datetime.now)
    created_at      = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at      = models.DateTimeField(_('updated at'))
    markup          = models.CharField(_(u"Post Content Markup"), max_length=3,
                              choices=markup_choices,
                              null=True, blank=True)
    tags            = TagField()

    # GeoDjango Fields
    point = models.PointField(blank=True, null=True)
    zoom = models.PositiveIntegerField(default=3, null=True, blank=True)
    objects = models.GeoManager()

    class Meta:
        verbose_name        = _('post')
        verbose_name_plural = _('posts')
        ordering            = ('-publish',)
        get_latest_by       = 'publish'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('blog_post', None, {
            'username': self.author.username,
            'year': self.publish.year,
            'month': "%02d" % self.publish.month,
            'slug': self.slug
    })
    get_absolute_url = models.permalink(get_absolute_url)
    def save(self, force_insert=False, force_update=False):
        print "HOAISJDOIJEOIENF"
        print self.id
        self.updated_at = datetime.now()
        super(Post, self).save(force_insert, force_update)
        from points.models import Point
        from django.contrib.contenttypes.models import ContentType
        if not Point.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                object_id = self.id,
                ):
            p=Point(zoom=self.zoom, point=self.point,
                    owner=self.author, object_id=self.id,
                    content_type=ContentType.objects.get_for_model(self),
            )
            p.save()


# handle notification of new comments
from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Post):
        post = instance.content_object
        if notification:
            notification.send([post.author], "blog_post_comment",
                {"user": instance.user, "post": post, "comment": instance})
models.signals.post_save.connect(new_comment, sender=ThreadedComment)
