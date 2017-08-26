from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'process_login', views.process_login, name='process_login'),
    url(r'add_keyword', views.add_keyword, name='add_keyword'),
    url(r'search/(?P<keyword_id>\d+)$', views.search, name='search'),
    url(r'searchresults$', views.searchresults, name='searchresults'),
    url(r'get_searchresults_csv', views.get_searchresults_csv, name='get_searchresults_csv'),
]