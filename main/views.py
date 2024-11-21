from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import *


class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'tasks': Task.objects.filter(user=request.user),
        }
        return render(request, 'home.html', context)


class DeleteConfirmationView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if task is None:
            return redirect('home')
        context = {
            'task': task,
        }
        return render(request, 'confirm_delete.html', context)

    def post(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        task.delete()
        return redirect('home')


class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add_task.html')

    def post(self, request):
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            user=request.user
        )
        return redirect('home')


class TaskEditView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if task is None:
            return redirect('home')
        context = {
            'task': task,
        }
        return render(request, 'edit_task.html', context)

    def post(self, request, task_id):
        task = Task.objects.get(pk=task_id, user=request.user)
        if task is None:
            return redirect('home')
        task.title = request.POST['title']
        task.description = request.POST['description']
        if request.POST.get('completed'):
            task.completed = True
        else:
            task.completed = False
        task.save()
        return redirect('home')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'register.html')

    def post(self, request):
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
            login(request, user)
            return redirect('home')
        else:
            return redirect('register')
