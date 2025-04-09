import csv
from datetime import datetime

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import HasPermission
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateAPIView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permissions = ['view_task']

    def get_permissions(self):
        if self.request.method == 'POST':
            self.required_permissions = ['create_task']
        return super().get_permissions()


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasPermission]
    required_permissions = ['view_task']

    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            self.required_permissions = ['update_task']
        elif self.request.method == 'DELETE':
            self.required_permissions = ['delete_task']
        return super().get_permissions()


class AssignedTaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    required_permissions = ['view_task']

    def get_queryset(self):
        return super().get_queryset().filter(assigned_to=self.kwargs.get('user_id'))


class AcceptTaskAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            task_id = kwargs.get('pk')

            task = Task.objects.filter(assigned_to=request.user).get(id=task_id)
            task.status = Task.Status.ACCEPTED
            task.save()

            return Response({'message': 'Task accepted'})
        except Task.DoesNotExist:
            return Response(
                data={'message': 'Task does not exists'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TaskReportAPIView(APIView):
    permission_classes = (IsAuthenticated, HasPermission)
    required_permissions = ['generate_report']
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if not start_date or not end_date:
            return Response(
                data={'message': 'Start date and end date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        tasks = (Task.objects.select_related('created_by', 'assigned_to')
                 .filter(created_at__gte=start_date.date())
                 .filter(created_at__lte=end_date.date())
                 .all())

        response = HttpResponse(content_type='text/csv')
        filename = f'{start_date}-{end_date}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'ID',
            'Title',
            'Description',
            'Created By',
            'Assigned To',
            'Status',
            'Priority',
            'Deadline',
            'Created At',
        ])

        for task in tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.created_by.name,
                task.assigned_to.name,
                task.status,
                task.priority,
                task.deadline,
                task.created_at,
            ])

        return response
