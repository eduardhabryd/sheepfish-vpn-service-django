from django.urls import path
from vpn_app.views import SiteListView

urlpatterns = [
    path('', SiteListView.as_view()),
]
