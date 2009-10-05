from datetime import datetime

from django.contrib.gis.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from tagging.fields import TagField
from photos.models import Pool

from django.template.defaultfilters import slugify

from points.models import Point

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

from wiki.views import get_articles_for_object

class Tribe(models.Model):
    """
    a tribe is a group of users with a common interest
    """

    slug = models.SlugField(_('slug'), max_length=200, unique=True)
    name = models.CharField(_('name'), max_length=200, unique=True)
    creator = models.ForeignKey(User, related_name="created_groups", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    description = models.TextField(_('description'))
    members = models.ManyToManyField(User, verbose_name=_('members'))
    
    deleted = models.BooleanField(_('deleted'), default=False)
    
    tags = TagField()
    
    photos = generic.GenericRelation(Pool)

    points = generic.GenericRelation(Point)

    class Meta:
        ordering=('-created',)
    
    # @@@ this might be better as a filter provided by wikiapp
    def wiki_articles(self):
        return get_articles_for_object(self)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ("tribe_detail", [self.slug])
    get_absolute_url = models.permalink(get_absolute_url)

    def save(self, force_insert=False, force_update=False):
        self.slug = self.slug.replace('-','_')
        super(Tribe, self).save(force_insert, force_update) # Call the "real" save() method.


class Topic(models.Model):
    """
    a discussion topic for the tribe.
    """
    
    tribe = models.ForeignKey(Tribe, related_name="topics", verbose_name=_('tribe'))
    title = models.CharField(_('title'), max_length=200)

    # add slug
    slug = models.SlugField(blank=True, null=True, editable=False, max_length=200)


    creator = models.ForeignKey(User, related_name="created_topics", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    modified = models.DateTimeField(_('modified'), default=datetime.now) # topic modified when commented on
    body = models.TextField(_('body'), blank=True)
    
    tags = TagField()
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ("tribe_topic", [self.tribe.slug, self.slug])
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        ordering = ('-modified', )
        # unique_together for url
        unique_together = (('tribe', 'slug'),)

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.title)
        super(Topic, self).save(force_insert, force_update) # Call the "real" save() method.



from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Topic):
        topic = instance.content_object
        topic.modified = datetime.now()
        topic.save()
        if notification:
            notification.send([topic.creator], "tribes_topic_response", {"user": instance.user, "topic": topic})
models.signals.post_save.connect(new_comment, sender=ThreadedComment)
