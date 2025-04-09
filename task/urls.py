from django.urls import path

from .views import (
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    AssignedTaskListAPIView,
    AcceptTaskAPIView,
    TaskReportAPIView
)

urlpatterns = [
    path('', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-retrieve-update-delete'),
    path('assigned/<int:user_id>/', AssignedTaskListAPIView.as_view(), name='assigned-task-list'),
    path('assigned/<int:pk>/accept/', AcceptTaskAPIView.as_view(), name='task-accept'),
    path('report/', TaskReportAPIView.as_view(), name='task-report'),
]
