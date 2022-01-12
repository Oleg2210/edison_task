from django.urls import path
from .views import PsychicsView

app_name = 'psychics'

urlpatterns = [
    path('', PsychicsView.as_view(), name='index_url')
]