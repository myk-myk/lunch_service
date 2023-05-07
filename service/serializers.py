from rest_framework import serializers
from service.models import ServiceUser, Restaurant, RestAddresses, WorkingHours, MenuDish, Vote


class ServiceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUser
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class RestAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestAddresses
        fields = '__all__'


class WorkingHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = '__all__'


class MenuDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDish
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    class Meta:
        model = Vote
        fields = '__all__'
