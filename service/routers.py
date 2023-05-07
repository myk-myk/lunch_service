from rest_framework import routers
from service.views import ServiceUserViewSet, RestaurantViewSet, RestAddressesViewSet, WorkingHoursViewSet, \
    MenuDishViewSet, VoteViewSet


router = routers.DefaultRouter()
router.register(r'service_user', ServiceUserViewSet)
router.register(r'restaurant', RestaurantViewSet, basename='restaurant')
router.register(r'rest_address', RestAddressesViewSet, basename='rest_address')
router.register(r'working_hours', WorkingHoursViewSet, basename='working_hours')
router.register(r'menu_dish', MenuDishViewSet, basename='menu_dish')
router.register(r'vote', VoteViewSet, basename='vote')
