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
    path("company_questions/<str:company>", views.company_questions, name="company_questions"),
    path("accounts/verify", views.verify, name="verify"),
    path("new_question/", views.new_question, name="new_question"),
    path("verify_email/<str:uid64>/<str:token>/", views.verify_email, name="verify_email"),
    path("add_company", views.add_company, name="add_company"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)