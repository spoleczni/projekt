from django.conf.urls import patterns, include, url
from django.contrib import admin
#import account

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spoleczni.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #grappelli    
    url(r'^grappelli/', include('grappelli.urls')),

    #ckeditor
    url(r'^ckeditor/', include('ckeditor.urls')),

    url(r'^$', 'spoleczni.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),

    #account urls
    url(r'^account/', include('account.urls')),

    #articles urls
    url(r'^articles/', include('articles.urls', namespace='articles')),

    #articles urls
    url(r'^videos/', include('video.urls', namespace='videos')),

    url(r"^ratings/", include("pinax.ratings.urls")),
    

    #url(r'^account/register/', 'account.views.register', name='register'),
    #url(r'^account/sign_in/', 'account.views.sign_in', name='sign_in'),
    #url(r'^account/lost_password/', 'account.views.lost_password', name='lost_password'),
    #url(r'^account/sign_out/', 'account.views.sign_out', name='sign_out'),
    #url(r'^account/edit/', 'account.views.edit', name='edit'),
    #url(r'^account/$', 'account.views.sign_in', name='sign_in'),

)
