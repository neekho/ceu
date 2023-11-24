from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

#CLASS BASED VIEWS
from rest_framework.views import APIView
from rest_framework import generics


# Models
from django.contrib.auth.models import User
from student.models import Student


# Serializers
from . serializers import StudentSerializer, UserSerializer


# Authentication/Permissions 
from rest_framework import permissions


# Nov 13/11/2023
# Error Handling, and JSON responses
# Serialization, Deserialization 
# Validation, and Auto Creation of a field e.x (Email for student)
# Postman



# age auto compute, and validate datetime's year
# Class Based Views (API View, Generics)
# Foreign Key, Authorization, and Permissions




@api_view(['GET'])
def overview(request):
    routes = {
        'List': '/students',
        'Detail-View': '/student/<str:pk>',
        'Create': '/student/add',
        'Update': '/student/update/<str:pk>',
        'Delete': '/student/delete/<str:pk>',

    }

    return Response(routes)


@api_view(['GET'])
def student_list(request):

    all_students = Student.objects.all()

    serializer = StudentSerializer(all_students, many=True)

    print(f'{serializer.data} content of serializer data.')
    print(type(serializer.data))

    return Response(serializer.data)

@api_view(['GET'])
def student(request, pk):

    try:

        student = Student.objects.get(id=pk)

        serializer = StudentSerializer(student, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Student.DoesNotExist:
        return Response({"error:" f"Student {pk} not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_student(request):

    # Wont work if may foreign key of creator na yung models
    # Will cause NOT NULL constraint failed: student_student.creator_id,
    # cause creator id is not known: TESTED ON POSTMAN

    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()
        print(f'{request.data} content of request.data')
        print(type(request.data))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        error_response = {"errors": "request failed!", "details": serializer.errors}
        print(serializer.errors)
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def update_student(request, pk):
    try:
        student = Student.objects.get(id=pk)

        serializer = StudentSerializer(instance=student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "update success"}, status=status.HTTP_200_OK)

        else:
            error_response = {"message": "update failed", "errors": serializer.errors}

            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
    except Student.DoesNotExist:
        return Response({"error:" f"Student ID of {pk} does not exists."}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['DELETE'])
def delete_student(request, pk):

    try:
        student = Student.objects.get(id=pk)
    
        student.delete()

        return Response({"message": f"Student with ID {pk} deleted"}, status=status.HTTP_200_OK)
    
    except Student.DoesNotExist:
        return Response({"error": f"Student with ID {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)



class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        

class StudentsView(APIView):

    '''
        List of students, or/and Add a student

        Authorization:
            Students objects are created by a logged in User.

            Only authenticated Users can create Student instances.
            
            Only the creator of a student instance may delete, or delete the object.


        permissions.IsAuthenticatedOrReadOnly:
            When you are not authenticated, then READ/GET REQUESTS only.
            When logged in or authenticated, then READ, WRITE AND DELETE REQUESTS are now available.

        
        NOTES: Once permissions are declared, you need to somehow provide your credentials in postman
        or simply use the browse-able api 

    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get(self, request):
        student = Student.objects.all()
        print('FROM class based view')

        serializer = StudentSerializer(student, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        print('from cbv post method')
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            print(self.request.user)
            print(f'{request.data} content of request.data')
            print(type(request.data))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            error_response = {"errors": "request failed!", "details": serializer.errors}
            print(serializer.errors)
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    

class StudentDetailView(APIView):

    '''
        Working with single instances of Student
        Detailed view, update, and delete only for DetailViews
    
    '''

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Student.objects.get(id=pk)
        except Student.DoesNotExist:
            print('not found')
            raise Http404("Student not found")


    def get(self, request, pk):
        student = self.get_object(pk)

        serializer = StudentSerializer(student)

        return Response(serializer.data)
    
    def put(self, request, pk):
        student = self.get_object(pk)

        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "student updated"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    def delete(self, request, pk):
        student = self.get_object(pk)

        student.delete()

        return Response({"message": f"Student of {pk} was deleted."}, status=status.HTTP_204_NO_CONTENT)

