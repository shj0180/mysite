from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('specifics/<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('oper', views.operlinux, name='operlinux'),
    path('user', views.mock_user, name='mock_user'),
    path('activeapp', views.active_app, name='active_app'),
]


