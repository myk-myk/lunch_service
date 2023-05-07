from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from service.models import ServiceUser


GROUPS = ["Staff", "Employees"]
MODELS = ["serviceuser", "restaurant", "restaddresses", "workinghours", "menudish", "vote"]
PERMISSIONS = ["add", "view", "change", "delete"]


class Command(BaseCommand):
    help = "Create default groups"

    def handle(self, *args, **options):
        for group_name in GROUPS:
            group, created = Group.objects.get_or_create(name=group_name)
            if group.name == "Staff":
                user_queryset = ServiceUser.objects.filter(is_staff=True, is_superuser=False)
                for user in user_queryset:
                    user.groups.add(group)
                for model in MODELS:
                    for perm_name in PERMISSIONS:
                        codename = perm_name + "_" + model
                        try:
                            contenttype = ContentType.objects.get(app_label="service", model=model)
                            perm = Permission.objects.get(codename=codename, content_type=contenttype)
                            group.permissions.add(perm)
                        except PermissionError:
                            self.stdout.write(codename + " not found.")
            elif group.name == "Employees":
                user_queryset = ServiceUser.objects.filter(is_staff=False, is_superuser=False)
                for user in user_queryset:
                    user.groups.add(group)
                codenames = ["add_vote", "change_vote", "delete_vote",
                             "add_serviceuser", "change_serviceuser", "delete_serviceuser"]
                for model in MODELS:
                    codenames.append(f"view_{model}")
                for codename in codenames:
                    model = codename.split("_")[-1]
                    try:
                        contenttype = ContentType.objects.get(app_label="service", model=model)
                        perm = Permission.objects.get(codename=codename, content_type=contenttype)
                        group.permissions.add(perm)
                    except PermissionError:
                        self.stdout.write(codename + " not found")
