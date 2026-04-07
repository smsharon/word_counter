from django.urls import path
from .views import analyze_text, get_history, get_single_analysis

urlpatterns = [
    path('analyze-text/', analyze_text),
    path('history/', get_history),
    path('history/<int:id>/', get_single_analysis),
    
]