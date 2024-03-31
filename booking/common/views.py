from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic as views


class IndexViewUser(views.TemplateView):
    template_name = 'index/../../templates/accounts/index_with_profile.html'


class IndexView(views.TemplateView):
    template_name = 'index/index.html'


# class IndexViewUser(views.TemplateView):
#     template_name = 'index/index_with_profile.html'
    # model = HttpResponse
    #
    # def get_queryset(self):
    #     queryset = {}
    #
    #     return queryset