import os

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _ # @@@ really should be ugettext

from django.contrib.auth.models import User

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

from threadedcomments.models import ThreadedComment

from topics.forms import TopicForm
from topics.models import Topic

def topics(request, group_slug=None, form_class=TopicForm, template_name="topics.html", bridge=None):

    try:
        group = bridge.get_group(group_slug)
    except ObjectDoesNotExist:
        raise Http404
    
    if not request.user.is_authenticated():
        is_member = False
    else:
        is_member = group.user_is_member(request.user)

    if request.method == "POST":
        if request.user.is_authenticated():
            if is_member:
                topic_form = form_class(request.POST)
                if topic_form.is_valid():
                    topic = topic_form.save(commit=False)
                    topic.group = group
                    topic.creator = request.user
                    topic.save()
                    request.user.message_set.create(message=_("You have started the topic %(topic_title)s") % {"topic_title": topic.title})
                    topic_form = form_class() # @@@ is this the right way to reset it?
            else:
                request.user.message_set.create(message=_("You are not a member and so cannot start a new topic"))
                topic_form = form_class()
        else:
            return HttpResponseForbidden()
    else:
        topic_form = form_class()


    topics = group.content_objects(Topic)

    return bridge.render(template_name, {
        "group": group,
        "topic_form": topic_form,
        "is_member": is_member,
        "topics": topics,
    }, context_instance=RequestContext(request))


def topic(request, topic_id, group_slug=None, edit=False, template_name="topic.html", bridge=None):
    topic = get_object_or_404(Topic, id=topic_id)

    try:
        group = bridge.get_group(group_slug)
    except ObjectDoesNotExist:
        raise Http404

    if (request.method == "POST" and edit == True and 
        (request.user == topic.creator or request.user == topic.group.creator)):
        topic.body = request.POST["body"]
        topic.save()
        return HttpResponseRedirect(topic.get_absolute_url())

    return bridge.render(template_name, {
        'topic': topic,
        'edit': edit,
        'group': group,
    }, context_instance=RequestContext(request))


def topic_delete(request, topic_id, group_slug=None, bridge=None):
    topic = Topic.objects.get(pk=topic_id)

    if (request.method == "POST" and (request.user == topic.creator or
        request.user == topic.group.creator)): 
        ThreadedComment.objects.all_for_object(topic).delete()
        topic.delete()

    return HttpResponseRedirect(request.POST["next"])
