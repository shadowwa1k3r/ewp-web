from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.models import User
from ewp_control_panel.models import ApiKey, PushNotification, StreamAudio, StreamAudioCategory, Book
from pure_pagination.mixins import PaginationMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from ewp_api.models import Apartment, Feedback, Council
import json
import requests
from sentry_sdk import capture_message


def my_custom_page_not_found_view(request):
    capture_message("Page not found!", level='error')
    return render(request, '404.html', {})


class IndexView(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('userlist'))


class UserListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 10
    template_name = 'userlist.html'

    def get_queryset(self):
        return User.objects.filter(is_staff=False).order_by('id')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user.html'


class FeedbackListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Feedback
    context_object_name = 'feedbacks'
    paginate_by = 10
    template_name = 'feedbacklist.html'

    def get_queryset(self):
        return Feedback.objects.order_by('-id')


class UserFeedbackList(LoginRequiredMixin, PaginationMixin, ListView):
    model = Feedback
    context_object_name = 'feedbacks'
    paginate_by = 10
    template_name = 'feedbacklist.html'

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['pk'])[0].feedback_set.all()


class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = Feedback
    template_name = 'feedback.html'

    def post(self, request, **kwargs):
        if request.POST.get('status') == 'opened':
            fb = Feedback.objects.get(id=kwargs['pk'])
            fb.status = True
            fb.save()
        return HttpResponseRedirect(self.request.path_info)


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
        response = requests.get('http://ads-api.ru/main/api?user=ergashbek007@mail.ru&token=ded6f8df91fec3a5844f870356aefd12&date1=2018-11-05+17:00:00&category_id=2,3')
        json_data = json.loads(response.text)
        Apartment.save_as_object(json_data)
        return render(request, 'apikey.html', {'status': True, 'key': key})


class PushNotificationView(LoginRequiredMixin, PaginationMixin, ListView):
    model = PushNotification
    context_object_name = 'pushs'
    paginate_by = 10
    template_name = 'push.html'

    def get_queryset(self):
        return PushNotification.objects.all().order_by('-id')

    def post(self, request):
        title = request.POST.get('title')
        body = request.POST.get('body')
        push = PushNotification(title=title, body=body)
        push.save()
        # return render(request, 'push.html', {'status': True})
        return redirect(reverse('push'))


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


class CouncilListView(ListView):
    template_name = 'councillist.html'
    model = Council
    paginate_by = 10
    context_object_name = 'councils'


class CouncilCreateView(DetailView):
    model = Council
    template_name = 'councilcreate.html'

    def post(self, request):
        return render(request, self.template_name, {})


class StreamOpenView(View):
    def post(self, request):
        if request.POST.get('play'):
            cat = StreamAudioCategory.objects.filter(id=request.POST.get('c_id'))[0]
            if cat.status:
                cat.status = False
            else:
                cat.status = True
            cat.save()
        return HttpResponseRedirect(reverse('audiolist', kwargs={'pk': request.POST.get('c_id')}))


class AudioStreamListView(ListView):
    model = StreamAudio
    context_object_name = 'audios'
    paginate_by = 10
    template_name = 'audiolist.html'

    def get_context_data(self, **kwargs):
        context = super(AudioStreamListView, self).get_context_data(**kwargs)
        context['c_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return StreamAudioCategory.objects.filter(id=self.kwargs['pk'])[0].streamaudio_set.all()


class AudioStreamGroupListView(ListView):
    model = StreamAudioCategory
    context_object_name = 'categories'
    paginate_by = 10
    template_name = 'audiogrouplist.html'


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10
    template_name = 'booklist.html'
