from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from oauth2_provider.models import Application
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.utils import timezone
from datetime import timedelta
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

User = get_user_model()
password_reset_token_generator = PasswordResetTokenGenerator()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            auth_user = authenticate(username=user.username, password=password)
            
            if auth_user:
                # Get or create OAuth2 application
                app, created = Application.objects.get_or_create(
                    name="Default",
                    client_type=Application.CLIENT_CONFIDENTIAL,
                    authorization_grant_type=Application.GRANT_PASSWORD,
                )

                # Generate access token
                access_token = generate_token()
                refresh_token = generate_token()
                expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

                # Save the tokens
                app.accesstoken_set.create(
                    user=user,
                    token=access_token,
                    expires=expires,
                    scope='read write'
                )
                
                app.refreshtoken_set.create(
                    user=user,
                    token=refresh_token,
                    access_token=app.accesstoken_set.get(token=access_token),
                    application=app
                )

                return Response({
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    },
                    "tokens": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
                
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, 
                          status=status.HTTP_401_UNAUTHORIZED)


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


class DashboardView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']  # or ['write'] for write operations

    def get(self, request):
        # Your dashboard logic here
        return Response({
            "message": "Protected dashboard data",
            "user": request.user.email
        })


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, 
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the refresh token instance
            old_refresh_token = oauth2_settings.REFRESH_TOKEN_MODEL.objects.get(
                token=refresh_token
            )
            
            # Check if the refresh token has expired
            if old_refresh_token.access_token.expires < timezone.now():
                old_refresh_token.delete()
                return Response({"error": "Refresh token has expired"}, 
                              status=status.HTTP_401_UNAUTHORIZED)

            # Generate new tokens
            access_token = generate_token()
            new_refresh_token = generate_token()
            expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

            # Create new access token
            new_access_token = old_refresh_token.application.accesstoken_set.create(
                user=old_refresh_token.user,
                token=access_token,
                expires=expires,
                scope=old_refresh_token.access_token.scope
            )

            # Create new refresh token
            old_refresh_token.application.refreshtoken_set.create(
                user=old_refresh_token.user,
                token=new_refresh_token,
                access_token=new_access_token,
                application=old_refresh_token.application
            )

            # Delete old refresh token
            old_refresh_token.delete()

            return Response({
                "access_token": access_token,
                "refresh_token": new_refresh_token,
                "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            })

        except oauth2_settings.REFRESH_TOKEN_MODEL.DoesNotExist:
            return Response({"error": "Invalid refresh token"}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)