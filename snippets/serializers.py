from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        검증한 데이터로 새 `Snippet` 인스턴스를 생성하여 리턴합니다.
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

    """
    python manage.py shell
>>> from snippets.models import Snippet
>>> from snippets.serializers import SnippetSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser

* snippet 인스턴스 만들기
>>> snippet = Snippet(code='foo = "bar"\n')
>>> snippet.save()
>>> snippet = Snippet(code='print "hello, world"\n')
>>> snippet.save()
* 인스턴스 중 하나 직렬화(serializer) 하기 - 파이썬의 데이터 타입으로 변환된다.
>>> serializer = SnippetSerializer(snippet)
>>> serializer.data
{'pk': 2, 'title': '', 'code': 'print "hello, world"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
* 직렬화 과정 마무리하기 - json으로 변환한다.
>>> content = JSONRenderer().render(serializer.data)
>>> content
b'{"pk":2,"title":"","code":"print \\"hello, world\\"\\n","linenos":false,"language":"python","style":"friendly"}'
* 반직렬화 하기 - 파이썬의 데이터 타입을 분석(parse)한다.
>>> from django.utils.six import BytesIO
>>> stream = BytesIO(content)
>>> data = JSONParser().parse(stream)
* 반직렬화 마무리 - 데이터를 인스턴스화 한다.
>>> serializer = SnippetSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.validated_data
OrderedDict([('title', ''), ('code', 'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
>>> serializer.save()
<Snippet: Snippet object (3)>
* 쿼리셋의 직렬화 - many=True 추가하기
>>> serializer = SnippetSerializer(Snippet.objects.all(), many=True)
>>> serializer.data
[OrderedDict([('pk', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('pk', 2), ('title', ''), ('code', 'print "hello, world"\n'), ('linenos', False),
('language', 'python'), ('style', 'friendly')]), OrderedDict([('pk', 3), ('title', ''), ('code', 'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
    """