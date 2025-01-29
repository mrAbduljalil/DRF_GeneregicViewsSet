from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class StudentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')

        # Kursga qo'shilgan talabalar sonini tekshirish
        if course.students.count() >= 30:
            return Response({'error': 'Course already has 30 students, cannot add more.'}, status=400)

        try:
            student = Student.objects.get(id=student_id)
            if student.age < 16:
                return Response({'error': 'Student must be at least 16 years old to be added to a course'}, status=400)
            course.students.add(student)
            return Response({'status': 'student added to course'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)




class StudentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['first_name', 'last_name', 'age', 'grade']
    search_fields = ['first_name', 'last_name']
