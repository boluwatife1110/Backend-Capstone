from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken,
    TokenError,
)
from rest_framework import serializers as drf_serializers
from drf_spectacular.utils import extend_schema, inline_serializer

from users import serializers


# =========================================================
# REGISTER
# =========================================================

RegistrationSuccess = inline_serializer(
    name="RegistrationSuccess",
    fields={
        "message": drf_serializers.CharField(),
    },
)

RegistrationError = inline_serializer(
    name="RegistrationError",
    fields={
        "errors": drf_serializers.DictField(),
    },
)


@extend_schema(
    summary="Register a new user",
    description="This endpoint allows users to create a new account.",
    tags=["Authentication"],
    request=serializers.UserSerializer,
    responses={
        201: RegistrationSuccess,
        400: RegistrationError,
    },
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):

    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {"errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# =========================================================
# SIGN IN
# =========================================================

SignInRequest = inline_serializer(
    name="SignInRequest",
    fields={
        "email": drf_serializers.EmailField(),
        "password": drf_serializers.CharField(),
    },
)

SignInResponse = inline_serializer(
    name="SignInResponse",
    fields={
        "message": drf_serializers.CharField(),
        "access_token": drf_serializers.CharField(),
        "refresh_token": drf_serializers.CharField(),
    },
)

SignInUnauthorized = inline_serializer(
    name="SignInUnauthorized",
    fields={
        "error": drf_serializers.CharField(),
    },
)


@extend_schema(
    summary="Sign In",
    description="This endpoint allows users to sign in using email and password.",
    tags=["Authentication"],
    request=SignInRequest,
    responses={
        200: SignInResponse,
        401: SignInUnauthorized,
    },
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signin(request):

    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(
        request,
        email=email,
        password=password,
    )

    if user is not None:

        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Signin successful",
                "access_token": str(access),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"error": "Invalid credentials"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


# =========================================================
# LOGOUT
# =========================================================

LogoutRequest = inline_serializer(
    name="LogoutRequest",
    fields={
        "refresh_token": drf_serializers.CharField(),
    },
)

LogoutResponse = inline_serializer(
    name="LogoutResponse",
    fields={
        "message": drf_serializers.CharField(),
    },
)

LogoutError = inline_serializer(
    name="LogoutError",
    fields={
        "error": drf_serializers.CharField(),
    },
)


@extend_schema(
    summary="Logout",
    description="This endpoint logs out a user by blacklisting the refresh token.",
    tags=["Authentication"],
    request=LogoutRequest,
    responses={
        200: LogoutResponse,
        400: LogoutError,
    },
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):

    try:
        refresh_token = request.data.get("refresh_token")

        token = RefreshToken(refresh_token)

        token.blacklist()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK,
        )

    except TokenError:

        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_400_BAD_REQUEST,
        )