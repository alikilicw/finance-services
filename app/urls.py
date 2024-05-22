from django.urls import path
from .views import *


urlpatterns = [
    path('financial-table', get_financial_tables_),
    path('news', get_news),
]