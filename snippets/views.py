from rest_framework import generics
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

#새로 만든 serializer class를 view에서 어떻게 사용하는가!
#Class 기반 view형태 - generics
#기능들을 손쉽게 조합할 수 있다.
#Rest_Framework 에서 mixins와 연결된 generics view를 제공한다.


class SnippetList(generics.ListCreateAPIView):
    """
    코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer