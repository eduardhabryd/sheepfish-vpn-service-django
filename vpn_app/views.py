import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlparse, urlunparse, urljoin, quote
from bs4 import BeautifulSoup

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


@csrf_exempt
def site_proxy(request, user_site_name, routes_on_original_site=""):
    try:
        print(f"Request: {user_site_name}====={routes_on_original_site}")

        if "/" in user_site_name:
            split_user_site_name = user_site_name.split("/", 1)
            user_site_name = split_user_site_name[0]
            routes_on_original_site = split_user_site_name[1] + "/" + routes_on_original_site

        site = Site.objects.get(user=request.user, name=user_site_name)

        original_url = urljoin(site.url, routes_on_original_site)
        print(f"Original URL: {original_url}")

        response = requests.get(original_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup.find_all(href=True):
            if tag.name == 'link':
                url = urljoin(site.url, tag['href'])
                if tag['href'].startswith('http'):
                    tag['href'] = tag['href']
                else:
                    tag['href'] = url
            elif tag.name == 'script':
                url = urljoin(site.url, tag['href'])
                if tag['href'].startswith('http'):
                    tag['href'] = tag['href']
                else:
                    tag['href'] = url
            else:
                tag['href'] = f"/vpn/{user_site_name.rstrip('/')}{tag['href']}"

        for tag in soup.find_all(src=True):
            url = urljoin(site.url, tag['src'])
            tag['src'] = url

        modified_content = str(soup)

        return HttpResponse(modified_content)

    except Site.DoesNotExist:
        print(f"Site not found for user: {user_site_name}")
        return HttpResponse(
            f"Site not found\n"
            f"{user_site_name}=={routes_on_original_site}",
            status=404
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)
