from django.urls import path
from .views import *

urlpatterns = [
    path('propuestas/', PropuestaTesisViewList.as_view(), name='propuesta_list'),
    path('propuesta/<int:pk>/', PropuestaTesisViewDetail.as_view(), name='propuesta_detail'),
    path('lista/', TesisViewList.as_view(), name='tesis_list'),
    path('<int:pk>/', TesisViewDetail.as_view(), name='tesis_detail'),
    path('<int:pk>/observaciones/', ObservacionViewList.as_view(), name='observacion_list'),
    path('<int:pk>/observacion/<int:observacion_pk>/', ObservacionViewDetail.as_view(), name='observacion_detail'),
]
