from rest_framework import mixins
from rest_framework import generics
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

#새로 만든 serializer class를 view에서 어떻게 사용하는가!
#Class 기반 view형태 - Mixins
#기능들을 손쉽게 조합할 수 있다.
#GenericAPIView가 핵심기능을 제공하고 mixins이 .retrieve(), .update(), .destroy()기능을 제공한다.


class SnippetList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView ):
    """
    코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, pk, format=None):
        return self.destroy(request, *args, **kwargs)