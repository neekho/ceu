
from rest_framework import serializers

from django.contrib.auth.models import User
from student.models import Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

    creator = serializers.ReadOnlyField(source='creator.username')
    
    birth_date = serializers.DateField()


    def validate(self, data):   

        existing_student = Student.objects.filter(
            first_name=data['first_name'].title(),
            last_name=data['last_name'].title()
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
    


    def validate_birth_date(self, value):

        if value.year < 1975:
            raise serializers.ValidationError('invalid year')

        return value



    






class UserSerializer(serializers.ModelSerializer):

    # student = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())

    student = StudentSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'student']



# Model Name + Serializer
