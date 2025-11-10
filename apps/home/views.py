from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        # self.request.session["my_name"] = "asghar"
        # print(self.request.session.get("my_name"))
