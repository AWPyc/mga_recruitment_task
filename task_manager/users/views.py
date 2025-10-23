from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import viewsets
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from django.views.generic import CreateView
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserRegistration(CreateView):
    model = User
    fields = ['username', 'password', 'email']
    template_name = "registration/registration.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        password = form.cleaned_data['password']
        self.object = form.save(commit=False)
        self.object.set_password(password)

        return super().form_valid(form)
