from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import (
    dashboard_page,
    login_page,
    register_page,
    transactions_page,
)


urlpatterns = [

    # Dashboard
    path(
        "",
        dashboard_page,
        name="dashboard",
    ),

    # Admin
    path(
        "admin/",
        admin.site.urls,
    ),

    # Authentication APIs
    path(
        "api/accounts/",
        include("accounts.urls"),
    ),

    # Card APIs
    path(
        "api/cards/",
        include("cards.urls"),
    ),

    # Transaction APIs
    path(
        "api/transactions/",
        include("transactions.urls"),
    ),

    # JWT
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Frontend pages
    path(
        "login/",
        login_page,
        name="login-page",
    ),

    path(
        "register/",
        register_page,
        name="register-page",
    ),

    path(
        "transactions/",
        transactions_page,
        name="transactions-page",
    ),
]