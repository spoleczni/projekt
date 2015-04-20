from django.conf.urls import patterns, url
from account import views

urlpatterns = patterns('',
                      url(r'^register/$', views.register, name='register'),
                      url(r'^sign_in/$', views.sign_in, name='sign_in'),
                      url(r'^lost_password/$', views.lost_password, name='lost_password'),
                      url(r'^sign_out/$', views.sign_out, name='sign_out'),
                      url(r'^edit/', views.edit, name='edit'),
                      url(r'^edit/', views.write_article, name='succ'),
                      url(r'^write_article/', views.write_article, name='write_article'),
                      url(r'^editform/', views.editform, name='editform'),
                      url(r'^$', views.sign_in, name='sign_in'),
)
