from rest_framework import serializers
from .models import Project, ProjectType

class ProjectSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    #owner_name = serializers.CharField(source='owner.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)

  

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'estimated_end_date', 'updated_at', 'completed_at', 
                  'company_name', 'type_name', 'owner']
        
class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ['id', 'name',]
