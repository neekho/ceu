
from rest_framework import serializers

from django.contrib.auth.models import User
from student.models import Student


class UserSerializer(serializers.ModelSerializer):

    student = serializers.PrimaryKeyRelatedField(many=True, queryset= Student.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'student']



# Model Name + Serializer
class StudentSerializer(serializers.ModelSerializer):

    VALID_COURSE = ['BSIT', 'BSCS']

    creator = serializers.ReadOnlyField(source='creator.username')


    def validate(self, data):

        existing_student = Student.objects.filter(
            first_name=data['first_name'],
            last_name=data['last_name']
        ).exclude(id=self.instance.id if self.instance else None).first()



        VALID_COURSE = ['BSIT', 'BSCS']

        if data['course'] not in VALID_COURSE:
            raise serializers.ValidationError("Invalid Course")
        
        if existing_student:
            raise serializers.ValidationError(f" student already exists.")




        return data

    def validate_first_name(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError('first name is too short')
        
        return value
    



    class Meta:
        model = Student
        fields = [
            'creator',
            'id',
            'first_name',
            'last_name',
            'age',
            'email',
            'course'
        ]