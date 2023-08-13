from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
# from decouple import config
import random
import string

# KAKAO_CLIENT_ID = config('KAKAO_CLIENT_ID')
# KAKAO_REDIRECT_URI = config('KAKAO_REDIRECT_URI')

def generate_random_nickname():
    # 랜덤한 문자열을 생성하여 닉네임으로 사용
    letters = string.ascii_letters
    random_nickname = ''.join(random.choice(letters) for i in range(6))  # 6자리 랜덤 닉네임 생성
    return random_nickname

class KakaoLoginView(APIView):

    def get_user_info(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def post(self, request):
        authorization_code = request.data.get('authorization_code')  # 수정: 프론트엔드에서 인가 코드 전달

        # 카카오로 액세스 토큰 요청
        response = requests.post('https://kauth.kakao.com/oauth/token', data={
            'grant_type': 'authorization_code',
            'client_id': 'dc6d77371b58fce528a75d2f7504577c' ,
            'redirect_uri': 'http://localhost:3000/auth/api/kakao-login',
            'code': authorization_code,
        })

        if response.status_code == 200:
            access_token = response.json().get('access_token')
            user_info = self.get_user_info(access_token)
            if user_info:
                social_id = user_info.get('id')

                try:
                    user = User.objects.get(social_id=social_id)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'msg': '로그인 성공'
                    }, status=status.HTTP_200_OK)

                except User.DoesNotExist:
                    nick_name = generate_random_nickname()  # 랜덤 닉네임 생성
                    new_user = User.objects.create(
                        nick_name=nick_name,
                        social_id=social_id,  # 카카오 소셜 ID 저장
                        is_social=True,
                    )

                    refresh = RefreshToken.for_user(new_user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'msg': '카카오 회원가입 및 로그인 성공'
                    }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "액세스 토큰 발급 실패"}, status=status.HTTP_400_BAD_REQUEST)
        


