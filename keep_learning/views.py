from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class RootAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            data = {
                'account': request.build_absolute_uri('/account/'),
                'teacher': {
                    'class': request.build_absolute_uri('/classroom/'),
                }
            }
        else:
            data = {
                'login': reverse('token_obtain_pair', request=request),
                'refresh_token': reverse('token_refresh', request=request),
                'register_teacher': reverse('user-register-teacher', request=request),
                'browsable_api_login': reverse('rest_framework:login', request=request),
            }
        return Response(data)
