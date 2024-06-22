from django.contrib.auth.models import Group, Permission
from django.db import connection


def create_groups_and_permissions():
    group_permissions = {
        "company": [
            "view_internship",
            "view_usercustom",
            "view_contract",
            "view_contractsignature",
            "view_report",
            "view_reportsignature",
            "add_internship",
            "add_contract",
            "add_contractsignature",
            "add_reportsignature",
            "change_internship",
        ],
        "teacher": [
            "view_internship",
            "view_usercustom",
            "view_contract",
            "view_contractsignature",
            "view_report",
            "view_reportsignature",
            "view_collegeclass",
            "view_department",
            "add_internship",
            "add_contract",
            "add_contractsignature",
            "add_reportsignature",
            "change_internship",
            "delete_internship",
        ],
        "student": [
            "view_internship",
            "view_usercustom",
            "view_contract",
            "view_contractsignature",
            "view_report",
            "view_reportsignature",
            "view_collegeclass",
            "add_contractsignature",
            "add_reportsignature",
            "add_report",
            "change_report",
            "delete_report",
        ],
    }

    table_exists = "easyintern.auth_group" in connection.introspection.table_names()

    if table_exists:
        for group_name, perm_codenames in group_permissions.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            existing_permissions = set(
                group.permissions.values_list("codename", flat=True)
            )
            new_permissions = set(perm_codenames)

            if existing_permissions != new_permissions:
                group.permissions.clear()
                for perm_codename in perm_codenames:
                    permission = Permission.objects.filter(
                        codename=perm_codename
                    ).first()
                    if permission:
                        group.permissions.add(permission)
                group.save()
