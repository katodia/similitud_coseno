from rest_framework.serializers import ModelSerializer
from .models import Related

class RelatedSerializer(ModelSerializer):
    class Meta:
        model = Related
        fields = ('related', 'value')
        depth = 1
