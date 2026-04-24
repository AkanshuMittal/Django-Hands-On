# from .models import Student
# from .serializers import StudentSerializer
# from rest_framework import viewsets
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# #from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# #from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
# #from .custompermissions import MyPermission

# Create your views here.
# class StudentModelViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     #authentication_classes = [BasicAuthentication, SessionAuthentication]
#     #permission_classes = [IsAuthenticated]
#     #permission_classes = [IsAdminUser]
#     #permission_classes = [IsAuthenticatedOrReadOnly]
#     #permission_classes = [DjangoModelPermissions]
#     #permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
#     #permission_classes = [MyPermission]


## For Filtering
from .serializers import StudentSerializer
from rest_framework.generics import ListAPIView
from .models import Student

# class StudentList(ListAPIView):
#     # queryset = Student.objects.all()
#     queryset = Student.objects.filter(passby='Akanshu')
#     serializer_class = StudentSerializer
#     def get_queryset(self):
#         user =self.request.user
#         return Student.objects.filter(passby=user)

## DjangoFilterBackend
# class StudentList(ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     filterset_fields = ['city']

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = ['city', 'name']


class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['city', 'name']

class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'name']
    search_fields = ['city', 'name']
    ordering_fields = ['city', 'name']

    

