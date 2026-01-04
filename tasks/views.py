from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import Task


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")   # ✅ ALWAYS redirect after success
        else:
            # 🔴 IMPORTANT: show errors
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, "tasks/register.html", {"form": form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)   # ✅ logs in THAT specific user
            return redirect("task_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "tasks/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(title=title, created_by=request.user)
        return redirect("task_list")

    tasks = Task.objects.filter(created_by=request.user).order_by("-id")
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required(login_url="login")
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)

    # Toggle completion
    task.completed = not task.completed
    task.save()

    return redirect("task_list")

@login_required(login_url="login")
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully")
    return redirect("task_list")