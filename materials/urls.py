from django.urls import path
from rest_framework.routers import DefaultRouter
from materials.apps import MaterialsConfig

from materials.views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonUpdateApiView, \
    LessonDestroyApiView, LessonRetrieveApiView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register('', CourseViewSet)
urlpatterns = [
    path('lessons/', LessonListApiView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson_retrieve'),
    path('lessons/create/', LessonCreateApiView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/update/', LessonUpdateApiView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson_delete'),

]
urlpatterns += router.urls
