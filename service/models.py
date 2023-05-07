from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

# Create your models here.
WEEKDAYS = [
  ('Monday', "Monday"),
  ('Tuesday', "Tuesday"),
  ('Wednesday', "Wednesday"),
  ('Thursday', "Thursday"),
  ('Friday', "Friday"),
  ('Saturday', "Saturday"),
  ('Sunday', "Sunday"),
]

DISH_CATEGORY = [
  ('soup', "First dish"),
  ('main', "Main dish"),
  ('meat', "Meat"),
  ('garnish', "Garnish"),
  ('salad', "Salad"),
  ('dessert', "Dessert"),
  ('hot_dr', "Hot drink"),
  ('cold_dr', "Cold drink"),
  ('alco', "Alcohol"),
  ('add', "Addition"),
]

MODELS = ["user", "restaurant", "address", "restaurant working time", "dish", "vote"]
PERMISSIONS = ["add", "view", "change", "delete"]


class ServiceUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), unique=True, max_length=32,
                                help_text=_("Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only."),
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                    'invalid': _("Username is incorrect.")
                                },
                                validators=[UnicodeUsernameValidator()])
    first_name = models.CharField(_("name"), max_length=64)
    last_name = models.CharField(_("surname"), max_length=128)
    phone_number = models.CharField(_("phone number"), unique=True, max_length=16,
                                    help_text=_("Non-required. 7-15 characters valid number. Digits and + only."),
                                    error_messages={
                                        'invalid': _("Phone number is incorrect."),
                                    },
                                    validators=[RegexValidator(regex='^[+]?[0-9]{7,15}$',
                                                               message=_("Phone number should be a 7-15 characters valid number which starts with '+' sign."))])
    email = models.EmailField(_("email"), unique=True, max_length=256,
                              help_text=_("Non-required. 256 characters or fewer. Letters, digits and @/./+/-/_ only."),
                              error_messages={
                                  'unique': _("A user with that email already exists."),
                                  'invalid': _("Email address is incorrect.")
                              })
    vacancy = models.CharField(_("vacancy"), max_length=256, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active. "
                    "Unselect this instead of deleting accounts."),)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Restaurant(models.Model):
    name = models.CharField(_("name"), unique=True, max_length=64,
                            help_text=_("Required. 64 characters or fewer. Letters, digits and @/./+/-/_ only."),
                            error_messages={
                                'unique': _("A user with that username already exists."),
                            })
    content = models.TextField(_("description"), blank=True)
    phone_number = models.CharField(_("phone number"), unique=True, max_length=16,
                                    help_text=_("Required. 7-15 characters valid number. Digits and + only."),
                                    error_messages={
                                        'invalid': _("Phone number is incorrect."),
                                    },
                                    validators=[RegexValidator(regex='^[+]?[0-9]{7,15}$',
                                                               message=_("Phone number should be a 7-15 characters valid number which starts with '+' sign."))])
    email = models.EmailField(_("email"), blank=True, unique=True, max_length=256,
                              help_text=_('Required. 256 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                              error_messages={
                                  'unique': _("A user with that email already exists."),
                                  'invalid': _("Email address is incorrect.")
                              })
    upload_time = models.DateTimeField(_("upload datetime"), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")


class RestAddresses(models.Model):
    city = models.CharField(_("city"), max_length=64)
    district = models.CharField(_("district"), max_length=128)
    street = models.CharField(_("street"), max_length=256)
    building_number = models.CharField(_("building number"), max_length=8)
    floor = models.PositiveSmallIntegerField(_("floor number"), blank=True, null=True)
    room = models.PositiveSmallIntegerField(_("apartment number"), blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, to_field='name', related_name='addresses',
                                   on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.city} {self.street} {self.building_number}"

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")


class WorkingHours(models.Model):
    weekday = models.CharField(_("day"), choices=WEEKDAYS)
    from_hour = models.TimeField(_("start time"))
    to_hour = models.TimeField(_("end time"))
    restaurant = models.OneToOneField(Restaurant, to_field='name', on_delete=models.CASCADE, related_name='rest_working_hours')
    rest_address = models.OneToOneField(RestAddresses, on_delete=models.CASCADE, related_name='addr_working_hours')

    def __str__(self):
        return f"{self.weekday}: {self.from_hour} - {self.to_hour}"

    class Meta:
        verbose_name = _("restaurant working time")
        verbose_name_plural = _("restaurants working time")


class MenuDish(models.Model):
    title = models.CharField(_("dish name"), max_length=128)
    content = models.TextField(_("description"), blank=True)
    category = models.CharField(_("dish category"), choices=DISH_CATEGORY)
    price = models.DecimalField(_("price"), max_digits=7, decimal_places=2)
    weight = models.PositiveSmallIntegerField(_("portion weight"), blank=True)
    size = models.CharField(_("portion size"), max_length=3, blank=True)
    upload_time = models.DateTimeField(_("upload datetime"), auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, to_field='name', related_name='dishes',
                                   on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.restaurant.name}, {self.title}"

    class Meta:
        verbose_name = _("dish")
        verbose_name_plural = _("dishes")


class Vote(models.Model):
    value = models.BooleanField(_("vote"), default=True)
    vote_time = models.DateTimeField(_("vote datetime"), auto_now_add=True)
    user = models.ForeignKey(ServiceUser, to_field='username', related_name='users',
                             on_delete=models.CASCADE, null=True)
    restaurant = models.ForeignKey(Restaurant, to_field='name', related_name='restaurants',
                                   on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(RestAddresses, related_name='addresses', on_delete=models.CASCADE, null=True)
    menu = models.ManyToManyField(MenuDish, related_name='dishes', db_table='menu_vote')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = _("vote")
        verbose_name_plural = _("votes")
