from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from oauth.serializer.kakao_oauth_access_token_serializer import KakaoOauthAccessTokenSerializer
from oauth.serializer.kakao_oauth_serializer import KakaoOauthUrlSerializer
from oauth.service.oauth_service_impl import OauthServiceImpl
from django.http import JsonResponse

# Google Oauth 등이 있으므로 사실 Kakao Oauth라고 하는 것이 더 좋았을 것 같음



class OauthView(viewsets.ViewSet):

    oauthService = OauthServiceImpl.getInstance()

    # 사용자가 '카카오 로그인' 버튼을 눌러 요청시 로그인 경로를 리턴(backlog)
    def kakaoOauthURI(self, request):
        url = self.oauthService.kakaoLoginAddress()
        serializer = KakaoOauthUrlSerializer(data={'url': url})
        serializer.is_valid(raise_exception=True)
        print(f"validated_data: {serializer.validated_data}")
        return Response(serializer.validated_data)

    def kakaoAccessTokenURI(self, request):
        serializer = KakaoOauthAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        try:
            accessToken= self.oauthService.requestAccessToken(code)
            return JsonResponse({'accessToken': accessToken})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def kakaoUserInfoURI(self, request):
        accessToken = request.data.get('access_token')
        print(f'accessToken: {accessToken}')

        try:
            user_info = self.oauthService.requestUserInfo(accessToken)
            return JsonResponse({'user_info': user_info})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

