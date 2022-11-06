from django.http import HttpResponse
from django.template import loader
from rest_framework.viewsets import ModelViewSet
from .models import Related
from .serializers import RelatedSerializer
from .models import Course

class RelatedViewSet(ModelViewSet):
    serializer_class = RelatedSerializer

    def get_queryset(self):
        queryset = Related.objects.all()

        if course_id := self.request.query_params.get('course_id'):
            queryset = queryset.filter(course_id=course_id)
        return queryset.order_by('-value')[1:11]


def index(request):
    the_courses = Course.objects.order_by('name').all()
    template = loader.get_template('index.html')
    context = {
        'courses': the_courses
    }
    return HttpResponse(template.render(context, request))


