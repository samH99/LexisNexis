from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'YodleeMobSec.views.index', name='index'),
    url(r'^Upload/$', 'YodleeMobSec.views.Upload', name='Upload'),
    url(r'^about/$', 'YodleeMobSec.views.about', name='about'),
    url(r'^error/$', 'YodleeMobSec.views.error', name='error'),
    url(r'^features/$', 'YodleeMobSec.views.features', name='features'),
    url(r'^StaticAnalyzer/$', 'StaticAnalyzer.views.StaticAnalyzer', name='StaticAnalyzer'),
    url(r'^ViewSource/$', 'StaticAnalyzer.views.ViewSource', name='ViewSource'),
    url(r'^Smali/$', 'StaticAnalyzer.views.Smali', name='Smali'),
    url(r'^Java/$', 'StaticAnalyzer.views.Java', name='Java'),
    url(r'^DynamicAnalyzer/$', 'DynamicAnalyzer.views.DynamicAnalyzer', name='DynamicAnalyzer'),
    url(r'^admin/', include(admin.site.urls)),
]
