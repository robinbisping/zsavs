# Django imports
from django.urls import path
from django.views.generic.base import RedirectView

# Application imports
from .views import SubscriptionListView, SubscriptionCreateView, SubscriptionUpdateView, SubscriptionDetailView,\
    SubscriptionCancelView, PlanListView

# URL patterns
urlpatterns = [
    path('home/', RedirectView.as_view(pattern_name='subscription_list', permanent=True), name='login_index'),
    path('abos/', SubscriptionListView.as_view(), name='subscription_list'),
    path('abo/abonnieren/', PlanListView.as_view(), name='plan_list'),
    path('abo/abonnieren/<plan_slug>/', SubscriptionCreateView.as_view(), name='subscription_create'),
    path('abo/<int:subscription_id>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('abo/<int:subscription_id>/bearbeiten/', SubscriptionUpdateView.as_view(), name='subscription_update'),
    path('abo/<int:subscription_id>/kuendigen/', SubscriptionCancelView.as_view(), name='subscription_cancel')
]
