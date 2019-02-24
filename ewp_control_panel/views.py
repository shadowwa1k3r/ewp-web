from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.models import User
from ewp_control_panel.models import ApiKey
from pure_pagination.mixins import PaginationMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class UserListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 15
    template_name = 'userlist.html'

    def get_queryset(self):
        return User.objects.filter(is_staff=False).order_by('id')


class ApiKeyView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            key = ApiKey.objects.all()[0]
        except IndexError:
            key = ''
        return render(request, 'apikey.html', {'key': key})

    def post(self, request):
        apikey = request.POST.get('api-key')
        ApiKey.objects.all().delete()
        key = ApiKey(key=apikey)
        key.save()
        return render(request, 'apikey.html', {'status': True, 'key': key})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('login')
        pwd = request.POST.get('password')
        user = authenticate(username=username, password=pwd)
        if user:
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return HttpResponseRedirect(reverse('userlist'))
        return render(request, 'login.html', {'error': True})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))
