from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

# @@@ these can be cleaned up a lot, made more generic and with better queries

def username_autocomplete_all(request):
    if request.user.is_authenticated():
        from django.contrib.auth.models import User
        #from basic_profiles.models import Profile
        from avatar.templatetags.avatar_tags import avatar
        q = request.GET.get("q")
        users = User.objects.all()
        content = []
        # @@@ temporary hack -- don't try this at home (or on real sites)
        for user in users:
            if user.username.lower().startswith(q):
                try:
                    profile = user.get_profile()
                    entry = "%s,,%s" % (
                        avatar(user, 40),
                        user.username,
                        #profile.location
                    )
                except: #Profile.DoesNotExist:
                    pass
                content.append(entry)
        response = HttpResponse("\n".join(content))
    else:
        response = HttpResponseForbidden()
    setattr(response, "djangologging.suppress_output", True)
    return response


def username_autocomplete_friends(request):
    if request.user.is_authenticated():
        from friends.models import Friendship
        #from profiles.models import Profile
        from avatar.templatetags.avatar_tags import avatar
        q = request.GET.get("q")
        friends = Friendship.objects.friends_for_user(request.user)
        content = []
        for friendship in friends:
            if friendship["friend"].username.lower().startswith(q):
                try:
                    profile = friendship["friend"].get_profile()
                    entry = "%s,,%s" % (
                        avatar(friendship["friend"], 40),
                        friendship["friend"].username,
                        #profile.location
                    )
                except: #Profile.DoesNotExist:
                    pass
                content.append(entry)
        response = HttpResponse("\n".join(content))
    else:
        response = HttpResponseForbidden()
    setattr(response, "djangologging.suppress_output", True)
    return response

def all_tags_autocomplete(request):
    from tagging.models import Tag
    q = request.GET.get("q")
    content = []
    for t in Tag.objects.filter(name__startswith=str(q)):
        entry = "%s" % t.name
        content.append(entry)

    response = HttpResponse("\n".join(content))
    return response


from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError 

def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

