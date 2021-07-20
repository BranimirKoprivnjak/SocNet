from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from django.db import IntegrityError
from django.views import generic
from braces.views import SelectRelatedMixin
from app.models import Post, Tag
from users.models import User, Follower
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

User = get_user_model()

class PostDetailView(SelectRelatedMixin, generic.DetailView):
    model = Post
    #select_related --> OneToOneField or a ForeignKey, prefetch_related -->ManyToManyField
    #select_related = ('user', 'likes', 'comments',)
    #prefetch_related = (Prefetch('Tag', queryset=Tag), select_related)
    template_name = 'app/post_detail.html'

    #SingleObjectMixin expects either slug or pk, not uuid
    def get_object(self, queryset=None):
        return Post.objects.get(uuid=self.kwargs.get("uuid"))


class ProfileView(generic.ListView):
    #model = Post
    template_name = "app/profile.html"
    #context_object_name = "profile"

    def get_queryset(self):
        try:
            self.user = User.objects.prefetch_related("posts", "following").get(
                #To access the url parameters in class based views
                identifier__iexact=self.kwargs.get("identifier")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.user.posts.all(), self.user.following.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = self.user
        return context

'''
{
    'paginator': None,
    'page_obj': None,
    'is_paginated': False,
    'object_list': (<QuerySet [<Post: john125This is a description>]>, <QuerySet [<Follower: john125>, <Follower: john125>]>),
    'profile': (<QuerySet [<Post: john125This is a description>]>, <QuerySet [<Follower: john125>, <Follower: john125>]>),
    'view': <app.views.ProfileView object at 0x00000214C8EFA880>,
    'account': <User: john125>
}
'''

class Follow(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("app:profile", kwargs={"identifier": self.kwargs.get("identifier")})

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, identifier=self.kwargs.get("identifier"))

        try:
            if not user == self.request.user:
                Follower.objects.create(user=user, follower=self.request.user)

        except IntegrityError:
            messages.warning(self.request, f"You're already following {user}!")

        else:
            messages.success(self.request, f"You are now following {user}!")

        return super().get(request, *args, **kwargs)

class Unfollow(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("app:profile", kwargs={"identifier": self.kwargs.get("identifier")})

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, identifier=self.kwargs.get("identifier"))

        try:
            following = Follower.objects.filter(
                user=user,
                follower=self.request.user
            ).get()

        except Follower.DoesNotExist:
            messages.warning(
                self.request,
                "You cannot unfollow user becose you're not following it!"
            )

        else:
            following.delete()
            messages.success(
                self.request,
                "You have successfully unfollowed this user."
            )
        return super().get(request, *args, **kwargs)
