from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

User = get_user_model()
password_reset_token_generator = PasswordResetTokenGenerator()


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('user_email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

        if user:
            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = password_reset_token_generator.make_token(user)
            reset_url = f"{request.build_absolute_uri('/reset-password')}?uid={uid}&token={token}"

            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n{reset_url}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)

        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid token or user ID"}, status=status.HTTP_400_BAD_REQUEST)

        if password_reset_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)