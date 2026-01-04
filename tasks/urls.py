from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("register/", views.register_view, name="register"),  # ✅ FIXED
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("task/update/<int:pk>/", views.task_update, name="task_update"),
    path("task/delete/<int:pk>/", views.task_delete, name="task_delete"),
]
