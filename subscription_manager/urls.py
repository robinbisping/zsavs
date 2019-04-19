from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse
from django.views.generic.base import RedirectView, TemplateView

import debug_toolbar

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='plan_list', permanent=True)),
    path('', include('subscription_manager.payment.urls')),
    path('', include('subscription_manager.subscription.urls')),
    path('', include('subscription_manager.user.urls')),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('400/', TemplateView.as_view(template_name='400.html')),
        path('403/', TemplateView.as_view(template_name='403.html')),
        path('404/', TemplateView.as_view(template_name='404.html')),
        path('500/', TemplateView.as_view(template_name='500.html'))
    ]
