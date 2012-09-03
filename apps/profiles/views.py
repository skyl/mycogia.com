from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from friends.forms import InviteFriendForm
from friends.models import FriendshipInvitation, Friendship

from microblogging.models import Following
from django.contrib.contenttypes.models import ContentType # SKYL


from profiles.models import Profile
from profiles.forms import ProfileForm
from points.models import Point
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from avatar.templatetags.avatar_tags import avatar
#from gravatar.templatetags.gravatar import gravatar as avatar

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


def profiles(request, template_name="profiles/profiles.html"):
    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-date_joined")
    elif order == 'name':
        users = users.order_by("username")
    return render_to_response(template_name, {
        'users':users,
        'order' : order,
        'search_terms' : search_terms
    }, context_instance=RequestContext(request))


def profile(request, username, template_name="profiles/profile.html"):
    other_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated():
        is_friend = Friendship.objects.are_friends(request.user, other_user)
        is_following = Following.objects.is_following(request.user, other_user)
        other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
        from_user = request.user
    else:
        other_friends = []
        is_friend = False
        is_me = False
        is_following = False
        from_user = None

    if is_friend:
        invite_form = None
        previous_invitations_to = None
        previous_invitations_from = None
    else:
        if request.user.is_authenticated() and request.method == "POST":
            if request.POST["action"] == "invite":
                invite_form = InviteFriendForm(request.user, request.POST)
                if invite_form.is_valid():
                    invite_form.save()
            else:
                invite_form = InviteFriendForm(request.user, {
                    'to_user': username,
                    'message': ugettext("Let's be friends!"),
                })
                if request.POST["action"] == "accept": # @@@ perhaps the form should just post to friends and be redirected here
                    invitation_id = request.POST["invitation"]
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.accept()
                            request.user.message_set.create(message=_("You have accepted the friendship request from %(from_user)s") % {'from_user': invitation.from_user})
                            is_friend = True
                            other_friends = Friendship.objects.friends_for_user(other_user)
                    except FriendshipInvitation.DoesNotExist:
                        pass
        else:
            invite_form = InviteFriendForm(request.user, {
                'to_user': username,
                'message': ugettext("Let's be friends!"),
            })
    previous_invitations_to =\
        FriendshipInvitation.objects.filter(to_user=other_user,\
                            from_user=from_user).exclude(status='8')
    previous_invitations_from =\
        FriendshipInvitation.objects.filter(to_user=request.user,\
                            from_user=other_user).exclude(status='8')

    if is_me:
        if request.method == "POST":
            if request.POST["action"] == "update":
                profile_form = ProfileForm(request.POST, instance=other_user.get_profile())
                if profile_form.is_valid():
                    profile = profile_form.save(commit=False)
                    profile.user = other_user
                    profile.save()
            else:
                profile_form = ProfileForm(instance=other_user.get_profile())
        else:
            profile_form = ProfileForm(instance=other_user.get_profile())
    else:
        profile_form = None

    # SKYL
    followers_count = Following.objects.filter(followed_object_id=other_user.id, followed_content_type=ContentType.objects.get_for_model(other_user)).count()
    following_count = Following.objects.filter(follower_object_id=other_user.id, follower_content_type=ContentType.objects.get_for_model(other_user)).count()


    return render_to_response(template_name, {
        "followers_count": followers_count,
        "following_count": following_count,
        "profile_form": profile_form,
        "is_me": is_me,
        "is_friend": is_friend,
        "is_following": is_following,
        "other_user": other_user,
        "other_friends": other_friends,
        "invite_form": invite_form,
        "previous_invitations_to": previous_invitations_to,
        "previous_invitations_from": previous_invitations_from,
    }, context_instance=RequestContext(request))


def map(request):
    user = User.objects.all()[0]
    profile = Profile.objects.all()[0]

    user_points = Point.objects.filter(
            content_type=ContentType.objects.get_for_model(user)
    )

    profile_points = Point.objects.filter(
            content_type=ContentType.objects.get_for_model(profile)
    )

    context = {'user_points': user_points, 'profile_points': profile_points }
    return render_to_response('profiles/map.html', context, context_instance=RequestContext(request))
