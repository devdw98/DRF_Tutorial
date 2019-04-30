from rest_framework import permissions
from rest_framework import generics
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route

#새로 만든 serializer class를 view에서 어떻게 사용하는가!
#Class 기반 view형태 - generics
#기능들을 손쉽게 조합할 수 있다.
#Rest_Framework 에서 mixins와 연결된 generics view를 제공한다.
#permission_classes = (permissions.IsAuthenticatedOrReadOnly,)는 인증받은 요청에 읽기와 쓰기 권한을 부여하고, 인증받지 않은 요청에 대해서는 읽기 권한만 부여함.

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        #url만들 때 reverse 함수를 사용한다.
        'users':reverse('user-list',request=request, format=format),
        'snippets':reverse('snippet-list',request=request, format=format)
    })

class SnippetViewSet(viewsets.ModelViewSet):
    """
    list, create, retrieve, update, destroy 기능을 자동으로 지원한다.
    highlight기능은 코드로 추가 작성해야한다.
    """
    queryset - Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

# @detail_route 데코레이터는 자동지원되지 않는 기능에 대해 사용한다.
# 기본적으로 GET요청에 응답하고, method 인자를 설정한다면 POST 요청에도 응답할 수 있다.
# 추가기능의 URL은 메서드 이름과 같다. 변경하고 싶으면 데코레이터에 url_path를 설정하면 된다.
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highilght(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet): #읽기 전용 기능으로 자동 지원
    """
    'list'와 'detail'기능을 자동으로 지원합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
