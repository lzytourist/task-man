from django.core.management import BaseCommand

from account.models import Permission, Role, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Creating permissions')

        Permission.objects.all().delete()
        permissions = [
            Permission(title='Create task', codename='create_task'),
            Permission(title='Update task', codename='update_task'),
            Permission(title='Delete task', codename='delete_task'),
            Permission(title='View task', codename='view_task'),
            Permission(title='Create user', codename='create_user'),
            Permission(title='Update user', codename='update_user'),
            Permission(title='Delete user', codename='delete_user'),
            Permission(title='View user', codename='view_user'),
            Permission(title='Send email', codename='send_email'),
            Permission(title='Generate report', codename='generate_report'),
            Permission(title='Create role', codename='create_role'),
            Permission(title='Update role', codename='update_role'),
            Permission(title='Delete role', codename='delete_role'),
            Permission(title='View role', codename='view_role'),
            Permission(title='Assign role', codename='assign_role'),
        ]
        Permission.objects.bulk_create(permissions)
        self.stdout.write('Done creating permissions')

        self.stdout.write('Creating admin role')
        Role.objects.all().delete()
        role = Role.objects.create(title='Admin', codename='admin')
        role.permissions.add(*permissions)
        self.stdout.write('Created admin role')

        self.stdout.write('Create admin user')
        User.objects.all().delete()
        User.objects.create_user(
            email='admin@mail.com',
            password='123',
            name='Admin',
            role=role
        )
        self.stdout.write('Created admin user')
