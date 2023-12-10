from django.shortcuts import redirect, render


from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView


# views that require authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


# making requests
import requests
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken



class MyLoginView(AuthLoginView):
    template_name = 'student/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Generate and store refresh token in the session
        user = self.request.user
        refresh_token = str(RefreshToken.for_user(user))
        self.request.session['refresh_token'] = refresh_token

        return response


class MyLogoutView(LogoutView):
    template_name = 'student/logout.html'

class HomeView(LoginRequiredMixin, View):
    template_name ='student/home.html'


    def get(self, request, *args, **kwargs):
        # Your logic for handling GET requests (e.g., rendering the home page)
        return render(request, self.template_name, context={})



@login_required(login_url='login')
def all_students(request):
    
    refresh = request.session.get('refresh_token')
    print('Refresh token:', refresh)

    if not refresh:
        # if refresh expires, require user to log in again
        print('Refresh token not found or expired')
        return redirect('login')
    
    refresh_token = RefreshToken(refresh)
    access_token = str(refresh_token.access_token)

    # Store the access token in the session
    request.session['access_token'] = access_token
    
    
    url = f'http://localhost:8000/api/cbv/students/'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Successful request, handle the response data
        data = response.json()
        print(data)

        return render(request, 'student/home.html', context={'students': data})
    else:
        # Handle errors
        print(f"Error: {response.status_code}, {response.text}")


@login_required(login_url='login')
def student(request, pk):
    
    refresh = request.session.get('refresh_token')
    # print('Refresh token:', refresh)

    if not refresh:
        # if refresh expires, require user to log in again
        print('Refresh token not found or expired')
        return redirect('login')
    
    refresh_token = RefreshToken(refresh)
    access_token = str(refresh_token.access_token)

    # Store the access token in the session
    request.session['access_token'] = access_token
    

    url = f'http://localhost:8000/api/cbv/student/{pk}'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Successful request, handle the response data
        data = response.json()
        print(data)

        return render(request, 'student/home.html', context={'search': data})
    else:
        # Handle errors
        print(f"Error: {response.status_code}, {response.text}")