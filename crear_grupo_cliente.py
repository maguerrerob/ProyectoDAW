from django.contrib.auth.models import Group

# Verificar si el grupo ya existe
group_name = 'cliente'
if not Group.objects.filter(name=group_name).exists():
    # Crear el grupo si no existe
    group = Group(name=group_name)
    group.save()
    print(f'Se ha creado el grupo "{group_name}"')
else:
    print(f'El grupo "{group_name}" ya existe')
