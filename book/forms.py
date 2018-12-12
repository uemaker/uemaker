from DjangoUeditor.widgets import UEditorWidget
from django import forms
from book.models import Book, Chapter
from book.utils import ChapterTreeUtil


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        is_update = True if instance and instance.pk else False


class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = ['pid', 'book_id', 'title', 'code', 'sort', 'content']
        widgets = {
            'book_id': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'sort': forms.TextInput(attrs={'class': 'form-control'}),
            'content': UEditorWidget(
                attrs={'width': '100%', 'height': 400, 'imagePath': 'upload/images/', 'filePath': 'upload/files/',
                       'toolbars': [[
                           'fullscreen', 'source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'fontborder',
                           'strikethrough',
                           'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote',
                           'pasteplain', '|',
                           'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|',
                           'simpleupload', 'insertimage', 'emotion', 'insertvideo', 'music', 'attachment', 'map', 'gmap',
                           'insertcode', 'webapp', 'pagebreak', 'template', '|', 'selectall', 'cleardoc'
                       ]]},
            ),

        }

    def __init__(self, *args, **kwargs):
        book_id = kwargs.pop('book_id', None)
        pid = kwargs.pop('pid', None)
        super(ChapterForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            pid = instance.pk
            book_id = instance.book_id

        self.fields['pid'] = forms.ChoiceField(label=u'上级分类', initial=pid,
                                               widget=forms.Select(attrs={'class': 'form-control'}))
        trees = ChapterTreeUtil.getChapterTree(book_id, 0, '|')
        trees = [('0', '顶级章节')] + trees
        self.fields['pid'].choices = trees
        self.fields['book_id'].initial = book_id

