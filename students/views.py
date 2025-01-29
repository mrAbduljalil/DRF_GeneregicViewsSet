from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer


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


