from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic as views


# TODO: ListView for offers

class IndexViewUser(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = 'accounts/index_with_profile.html'


class IndexView(views.TemplateView):
    template_user = 'accounts/index_with_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'index/index.html', {})
        else:
            return render(request, self.template_user)


