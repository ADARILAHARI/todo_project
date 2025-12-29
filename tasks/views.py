from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Count
from .forms import RegisterForm, TaskForm
from .models import Task


def register_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "tasks/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("task_list")
        messages.error(request, "Invalid username or password")

    return render(request, "tasks/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def analytics_view(request):
    user = request.user
    today = now().date()

    total = Task.objects.filter(created_by=user).count()
    completed = Task.objects.filter(created_by=user, completed=True).count()
    pending = Task.objects.filter(created_by=user, completed=False).count()

    priority_stats = Task.objects.filter(created_by=user).values("priority").annotate(count=Count("id"))
    overdue = Task.objects.filter(created_by=user, completed=False, due_date__lt=today).count()

    context = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "priority_stats": priority_stats,
        "overdue": overdue,
    }

    return render(request, "tasks/analytics.html", context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.save()
    else:
        task.completed = not task.completed
        task.save()

    return redirect("task_list")



@login_required(login_url="login")
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    task.delete()
    messages.success(request, "Task deleted")
    return redirect("task_list")

@login_required
def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(
                title=title,
                created_by=request.user
            )
        return redirect("task_list")

    tasks = Task.objects.filter(created_by=request.user).order_by("-id")
    return render(request, "tasks/task_list.html", {"tasks": tasks})
