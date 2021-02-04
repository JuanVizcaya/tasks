from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SearchTaskAPI, FillDummyAPI, TaskViewSet


tasks_router = DefaultRouter()
tasks_router.register('', TaskViewSet, basename='tasks')

urlpatterns = [
    path('tasks/', include(tasks_router.urls)),
    path('tasks/<str:pk>/', include(tasks_router.urls)),
    path('tasks/search', SearchTaskAPI.as_view(), name="search-task"),
    path('tasks/fill-dummy', FillDummyAPI.as_view(), name="fill-dummy")
]
