from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import PropuestaTesis, Tesis, Observacion
from .serializers import PropuestaTesisSerializer, TesisSerializer, ObservacionSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.authentication import CustomJWTAuthentication

#----------------------GENERAL----------------------
class GeneralViewList(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(GeneralViewList, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(tesista=self.request.user)
    
class GeneralViewDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        return super(GeneralViewDetail, self).get_permissions()

#----------------------PROPUESTAS----------------------
class PropuestaTesisViewList(GeneralViewList):
    serializer_class = PropuestaTesisSerializer
    queryset = PropuestaTesis.objects.all()

class PropuestaTesisViewDetail(GeneralViewDetail):
    queryset = PropuestaTesis.objects.all()
    serializer_class = PropuestaTesisSerializer

#----------------------TESIS----------------------
class TesisViewList(GeneralViewList):
    queryset = Tesis.objects.all()
    serializer_class = TesisSerializer

class TesisViewDetail(GeneralViewDetail):
    queryset = Tesis.objects.all()
    serializer_class = TesisSerializer

#----------------------OBSERVACIONES----------------------
class ObservacionViewList(GeneralViewList):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer

    def perform_create(self, serializer):
        tesis = Tesis.objects.get(pk=self.kwargs['pk'])
        serializer.save(escrita_por=self.request.user, tesis=tesis)

class ObservacionViewDetail(GeneralViewDetail):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer