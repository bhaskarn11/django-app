from django.urls import path
from . import views
from .views import SearchView

urlpatterns = [
    path('', views.index, name='index'),
    path('search', SearchView.as_view(template_name = 'ecomm/search-result.html'), name='search-result')
]