from django.urls import path
from vpn_app.views import SiteListView, SiteCreateView, SiteUpdateView, SiteDeleteView, site_proxy

urlpatterns = [
    path('', SiteListView.as_view(), name='index'),
    path('add_site/', SiteCreateView.as_view(), name='add_site'),
    path("update_site/<int:pk>/", SiteUpdateView.as_view(), name='update_site'),
    path("delete_site/<int:pk>/", SiteDeleteView.as_view(), name='delete_site'),
    path('<str:user_site_name>/<path:routes_on_original_site>/', site_proxy, name='site_proxy'),
]


app_name = 'vpn_app'
