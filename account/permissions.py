from django.contrib.auth.models import Permission,Group

def group_permissionOfcathegorie_piece():
    add_marque = Permission.objects.get(codename = 'add_marque')
    change_marque = Permission.objects.get(codename='change_marque')
    delete_marque = Permission.objects.get(codename='delete_marque')

    add_modele = Permission.objects.get(codename = 'add_modele')
    change_modele = Permission.objects.get(codename='change_modele')
    delete_modele = Permission.objects.get(codename='delete_modele')

    add_cathegorie = Permission.objects.get(codename='add_cathegorie')
    change_cathegorie = Permission.objects.get(codename='change_cathegorie')
    delete_cathegorie = Permission.objects.get(codename='delete_cathegorie')

    add_piece = Permission.objects.get(codename='add_piece')
    change_piece = Permission.objects.get(codename='change_piece')
    delete_piece = Permission.objects.get(codename='delete_piece')

    create_permission=[
        add_marque,
        change_marque,
        delete_marque,

        add_modele,
        change_modele,
        delete_modele,

        add_cathegorie,
        change_cathegorie,
        delete_cathegorie,

        add_piece,
        change_piece,
        delete_piece,
    ]

    AgentGourpPermission =Group(name='AgentGourpPermission')
    AgentGourpPermission.save()
    AgentGourpPermission.permissions.set(create_permission)

    return AgentGourpPermission

    