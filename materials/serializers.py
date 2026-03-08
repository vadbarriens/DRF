from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.validators import validate_link
from materials.models import Course, Lesson
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    validators = [validate_link]

    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'link': {'validators': [validate_link], 'required': False}
        }


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = SerializerMethodField()
    validators = [validate_link]
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = ['title', 'preview', 'description', 'lessons', 'lessons_count']
