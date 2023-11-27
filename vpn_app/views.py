from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic

from vpn_app.models import Site
from vpn_app.forms import SiteSearchForm


# def index(request):
#     user = request.user
#     return render(request, 'vpn_app/index.html', {'user': user})

class SiteListView(generic.ListView):
    model = Site
    template_name = 'vpn_app/index.html'
    queryset = Site.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_name = self.request.GET.get('site_name')
        context['search_form'] = SiteSearchForm(initial={'site_name': site_name})
        return context

    def get_queryset(self):
        form = SiteSearchForm(self.request.GET)
        if form.is_valid():
            site_name = form.cleaned_data['site_name']
            return Site.objects.filter(name__icontains=site_name)

        return self.queryset


# @login_required
# def personal_cabinet(request):
#     user = request.user
#     return render(request, 'vpn_app/personal_cabinet.html', {'user': user})
