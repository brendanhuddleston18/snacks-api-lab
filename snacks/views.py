from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from .models import Snack
from .serializer import SnackSerializer
from .permissions import IsOwnerOrReadOnly

class SnackList(ListCreateAPIView):
    queryset = Snack.objects.all()

    serializer_class = SnackSerializer

class SnackDetail(RetrieveDestroyAPIView):
    queryset = Snack.objects.all()
    
    serializer_class = SnackSerializer
    permission_classes = (IsOwnerOrReadOnly,)

