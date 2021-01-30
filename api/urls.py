from django.urls import path

from api.views import TaskAPI

urlpatterns = [
    path('tasks/', TaskAPI.as_view(), name="task")
]
