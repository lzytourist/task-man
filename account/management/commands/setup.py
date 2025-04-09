from django.core.management import BaseCommand
from django.db import connection, transaction

from account.models import Permission, Role, User


def truncate(model):
    cursor = connection.cursor()
    cursor.execute(f'TRUNCATE TABLE {model._meta.db_table} CASCADE')


def clean(models):
    for model in models:
        model.objects.all().delete()
        truncate(model)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stderr.write('Cleaning tables...')
        clean([User, Permission, Role])

        with transaction.atomic():
            self.stderr.write('Cleaning tables...')
            clean([User, Permission, Role])

            self.stdout.write('Creating permissions')
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
                Permission(title='View analytics', codename='view_analytics'),
            ]
            Permission.objects.bulk_create(permissions)
            self.stdout.write('Done creating permissions')

            self.stdout.write('Creating admin role')
            role = Role.objects.create(title='Admin', codename='admin')
            role.permissions.add(*permissions)
            self.stdout.write('Created admin role')

            self.stdout.write('Creating PM role')
            pm_role = Role.objects.create(title='Project Manager', codename='pm')
            pm_role.permissions.add(*Permission.objects.filter(codename__in=[
                'create_task',
                'update_task',
                'delete_task',
                'view_task',
                'create_user',
                'update_user',
                'delete_user',
                'view_user',
                'send_email',
                'generate_report',
                'view_role',
                'assign_role',
                'view_analytics'
            ]).values_list('id', flat=True))
            self.stdout.write('Created PM role')

            self.stdout.write('Creating Developer role')
            dev_role = Role.objects.create(title='Developer', codename='developer')
            dev_role.permissions.add(*Permission.objects.filter(codename__in=[
                'create_task',
                'update_task',
                'view_task',
                'send_email',
                'view_user',
            ]).values_list('id', flat=True))
            self.stdout.write('Created Developer role')

            self.stdout.write('Create admin user')
            user = User.objects.create_user(
                email='admin@mail.com',
                password='123',
                name='Admin',
                role=role
            )
            pm = User.objects.create_user(
                email='pm@mail.com',
                password='123',
                name='Project Manager',
                role=pm_role
            )
            dev = User.objects.create_user(
                email='dev@mail.com',
                password='123',
                name='Developer',
                role=dev_role
            )
            self.stdout.write('Created users')
            self.stdout.write('Admin')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write('Password: 123')

            self.stdout.write('Project Manager')
            self.stdout.write(f'Email: {pm.email}')
            self.stdout.write('Password: 123')

            self.stdout.write('Developer')
            self.stdout.write(f'Email: {dev.email}')
            self.stdout.write('Password: 123')
