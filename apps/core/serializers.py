from rest_framework import serializers
from apps.personas.models import Meta,Estrategia

class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estrategia
        fields = ['est_id','est_nombre']
        
class EstrateiaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Estrategia
        fields = [
            'est_nombre'
        ]