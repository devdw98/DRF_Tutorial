from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,blank=True,default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python',max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly',max_length=100)
    owner = models.ForeignKey('auth.User',related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField() #pygments 라이브러리 사용
    class Meta:
        ordering = ('created',)
    
    def save(self, *args, **kwargs):
        """
        pygments 라이브러리를 사용하여 하이라이트된 코드를 만든다.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title':self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

"""
db지우는 과정
rm -f tmp.db db.sqlite3 
rm -r snippets/migrations

db 생성
python manage.py makemigrations snippets
python manage.py migrate

API 테스트 하는데 사용할 사용자 계정 생성
python manage.py createsuperuser >> username, email, password 받음
"""