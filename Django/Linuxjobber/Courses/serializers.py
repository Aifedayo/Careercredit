from .models import *
from rest_framework import serializers

class GraderSerializer(serializers.ModelSerializer):
	class Meta:
		model = LabTask
		fields = "__all__"