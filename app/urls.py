from django.urls import path
from . import views

urlpatterns = [
    path('nlp', views.nlp_view),
    path('ai', views.ai_view)
]