from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

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
