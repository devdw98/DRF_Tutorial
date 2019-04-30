from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

#하이퍼링크로 API를 연결하기 위해서는 ModelSerializer >> HyperlinkedModelSerializer로 변경해야한다.
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    #직렬화에 ReadOnlyField가 사용될 때 언제나 읽기 전용이므로, 모델의 인스턴스를 업데이트할 때는 사용할 수 없다.
    owner = serializers.ReadOnlyField(source='owner.username') #== CharField(read_only=True)
    highlight = serializers.HyperlinkedIdentityField(view_name = 'snippet-highlight', format='html')
    class Meta:
        model = Snippet #Serializer class의 단축버전
        field = ('url','highlight','owner','title','code','linenos','language','style')

    def create(self, validated_data): 
        """
        검증한 요청 데이터에 더하여 'owner'필드도 전달한다.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        검증한 데이터로 기존 `Snippet` 인스턴스를 업데이트한 후 리턴합니다.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

#사용자를 보여주는 API
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    snippets은 사용자 모델과 반대방향으로 이루어져있어서
    ModelSerializer에 기본적으로 추가되지 않는다.
    따라서 명시적으로 필드를 지정해준다.
    """
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name = 'snippet-detail',read_only=True)

    class Meta:
        model = User
        fields = ('url','username','snippets')