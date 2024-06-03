from drf_spectacular.utils import extend_schema, extend_schema_view
from knox.views import LoginView, LogoutView, LogoutAllView
from rest_framework.authentication import BasicAuthentication

@extend_schema_view(
    post=extend_schema(operation_id='login')
)
class TokenLoginView(LoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = []
    pass


@extend_schema_view(
    post=extend_schema(operation_id='logout')
)
class TokenLogoutView(LogoutView):
    pass


@extend_schema_view(
    post=extend_schema(operation_id='logoutAll')
)
class TokenLogoutAllView(LogoutAllView):
    pass