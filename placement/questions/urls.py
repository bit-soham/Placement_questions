from django.urls import path #type: ignore
from allauth.account.views import SignupView #type: ignore
from . import views #type: ignore
from django.conf import settings #type: ignore
from django.conf.urls.static import static #type: ignore

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/register", views.register, name="register"),
    # path("company/<str:company>", views.company_view, name="company"),
    path("view_question/<question_id>", views.view_question, name="view_question"),
    path("company_questions/<str:company>", views.company_questions, name="company_questions"),
    path("accounts/verify", views.verify, name="verify"),
    path("verify_email/<str:uid64>/<str:token>/", views.verify_email, name="verify_email"),
    path("add_question", views.add_question, name="add_question"),
    path("add_company", views.add_company, name="add_company"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search_results, name="search_results")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)