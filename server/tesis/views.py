from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import PropuestaTesis, Tesis, Observacion
from .serializers import PropuestaTesisSerializer, TesisSerializer, ObservacionSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.authentication import CustomJWTAuthentication
from django.db.models import Q

#----------------------GENERAL----------------------
class GeneralViewList(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

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

    def get_queryset(self):
        user = self.request.user
        user_class_name = user.__class__.__name__  # Get the class name of the user

        if user_class_name == 'Coordinador':
            # Return all the Tesis that are linked to the Coordinaor's ProgAcad 
            return PropuestaTesis.objects.filter(tesista__prog_acad=user.prog_acad)
        elif user_class_name == 'Profesor':
            # Filter Tesis where the user is the asesor or one of the jurados
            return PropuestaTesis.objects.filter(posible_asesor=user)
        elif user_class_name == 'Tesista':
            # Filter Tesis where the user is the tesista
            return PropuestaTesis.objects.filter(tesista=user)
        else:
            # Return an empty queryset for other user classes
            return PropuestaTesis.objects.none()

class PropuestaTesisViewDetail(GeneralViewDetail):
    queryset = PropuestaTesis.objects.all()
    serializer_class = PropuestaTesisSerializer

#----------------------TESIS----------------------
class TesisViewList(GeneralViewList):
    serializer_class = TesisSerializer

    def get_queryset(self):
        user = self.request.user
        user_class_name = user.__class__.__name__  # Get the class name of the user

        if user_class_name == 'Coordinador':
            # Return all the Tesis that are linked to the Coordinaor's ProgAcad 
            return Tesis.objects.filter(tesista__prog_acad=user.prog_acad)
        elif user_class_name == 'Profesor':
            # Filter Tesis where the user is the asesor or one of the jurados
            return Tesis.objects.filter(
                Q(asesor=user) | 
                Q(jurado_1=user) | 
                Q(jurado_2=user) | 
                Q(jurado_3=user)
            )
        elif user_class_name == 'Tesista':
            # Filter Tesis where the user is the tesista
            return Tesis.objects.filter(tesista=user)
        else:
            # Return an empty queryset for other user classes
            return Tesis.objects.none()
        
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