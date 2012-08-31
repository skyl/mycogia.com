from django.template import Library
from django.conf import settings

register = Library()

@register.inclusion_tag("tag_app/tag_list.html")
def show_tags_for(obj, group=None):
    return {
        "obj": obj,
        "group": group,
        "MEDIA_URL": settings.MEDIA_URL,
    }

@register.inclusion_tag("tag_app/tag_count_list.html")
def show_tag_counts(tag_counts):
    return {"tag_counts": tag_counts}