import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from vpn_app.models import Site
from vpn_app.forms import SiteSearchForm, SiteCreateForm, SiteUpdateForm


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


class SiteCreateView(generic.CreateView):
    model = Site
    template_name = 'vpn_app/add_site.html'
    form_class = SiteCreateForm
    success_url = reverse_lazy('vpn_app:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SiteUpdateView(generic.UpdateView):
    model = Site
    template_name = 'vpn_app/add_site.html'
    form_class = SiteUpdateForm
    success_url = reverse_lazy('vpn_app:index')


class SiteDeleteView(generic.DeleteView):
    model = Site
    template_name = 'vpn_app/delete_site.html'
    success_url = reverse_lazy('vpn_app:index')


@csrf_exempt  # Use this decorator to disable CSRF protection for this view, as it's an external proxy
def site_proxy(request, user_site_name, routes_on_original_site):
    try:
        # Assuming you have a user-specific site with the given name
        site = Site.objects.get(user=request.user, name=user_site_name)

        # Construct the URL of the original site based on user input
        original_url = f"{site.url}/{routes_on_original_site}"

        # Fetch content from the original site
        response = requests.get(original_url)

        # Modify the content to replace external links with internal routing
        modified_content = response.text.replace('href="',
                                                 'href="/{}/{}/'.format(user_site_name, routes_on_original_site))

        return HttpResponse(modified_content)

    except Site.DoesNotExist:
        return HttpResponse("Site not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
