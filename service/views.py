from rest_framework import viewsets

# Create your views here.
from .models import ServiceUser, Restaurant, RestAddresses, WorkingHours, MenuDish, Vote
from .serializers import ServiceUserSerializer, RestaurantSerializer, RestAddressesSerializer, \
    WorkingHoursSerializer, MenuDishSerializer, VoteSerializer
from .permissions import UserIsAdminOrOwnerOrReadOnly, IsStaffOrReadOnly, IsStaffOrOwnerOrAuthenticatedOnly


class ServiceUserViewSet(viewsets.ModelViewSet):
    queryset = ServiceUser.objects.all()
    serializer_class = ServiceUserSerializer
    permission_classes = (UserIsAdminOrOwnerOrReadOnly, )

class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = (IsStaffOrReadOnly, )

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        restname = self.request.query_params.get('name')
        if restname is not None:
            queryset = queryset.filter(name=restname)
        return queryset


class RestAddressesViewSet(viewsets.ModelViewSet):
    serializer_class = RestAddressesSerializer
    permission_classes = (IsStaffOrReadOnly, )

    def get_queryset(self):
        queryset = RestAddresses.objects.all()
        rest_name = self.request.query_params.get('rest_name')
        city_name = self.request.query_params.get('city')
        district_name = self.request.query_params.get('district')
        if rest_name is not None:
            queryset = queryset.filter(restaurant__name=rest_name)
        if city_name is not None:
            queryset = queryset.filter(city=city_name)
        if district_name is not None:
            queryset = queryset.filter(district=district_name)
        return queryset


class WorkingHoursViewSet(viewsets.ModelViewSet):
    serializer_class = WorkingHoursSerializer
    permission_classes = (IsStaffOrReadOnly, )

    def get_queryset(self):
        queryset = WorkingHours.objects.all()
        rest_name = self.request.query_params.get('rest_name')
        weekday = self.request.query_params.get('weekday')
        if rest_name is not None:
            queryset = queryset.filter(restaurant__name=rest_name)
        if weekday is not None:
            queryset = queryset.filter(weekday=weekday)
        return queryset


class MenuDishViewSet(viewsets.ModelViewSet):
    serializer_class = MenuDishSerializer
    permission_classes = (IsStaffOrReadOnly, )

    def get_queryset(self):
        queryset = MenuDish.objects.all()
        category = self.request.query_params.get('category')
        rest_name = self.request.query_params.get('rest_name')
        date = self.request.query_params.get('date')
        if rest_name is not None:
            queryset = queryset.filter(restaurant__name=rest_name)
        if category is not None:
            queryset = queryset.filter(category=category)
        if date is not None:
            queryset = queryset.filter(upload_time__date=date)
        return queryset


class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = (IsStaffOrOwnerOrAuthenticatedOnly, )

    def get_queryset(self):
        queryset = Vote.objects.all()
        user = self.request.query_params.get('user')
        rest_name = self.request.query_params.get('rest_name')
        date = self.request.query_params.get('date')
        if rest_name is not None:
            queryset = queryset.filter(restaurant__name=rest_name)
        if user is not None:
            queryset = queryset.filter(user__username=user)
        if date is not None:
            queryset = queryset.filter(vote_time__date=date)
        return queryset
