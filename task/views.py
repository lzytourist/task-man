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
