from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from materials.models import Course, Lesson
from materials.paginators import CoursePagination, LessonPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve', 'partial_update']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
