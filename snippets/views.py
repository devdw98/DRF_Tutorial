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
    
#코드 조각의 하이라이트 버전에 대한 엔드 포인트 만들기
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

class SnippetList(generics.ListCreateAPIView):
    """
    코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    """
    사용자가 만든 코드 조각을 연결한다.
    """
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer