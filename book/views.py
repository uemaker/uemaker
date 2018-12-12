from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
import json

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView

from book.forms import BookForm, ChapterForm
from book.models import Book, Chapter
from book.utils import ChapterTreeUtil


class BookListView(ListView):
    template_name = 'book/book_list.html'
    context_object_name = "data"
    paginate_by = 100

    def post(self, request, *args, **kwargs):
        bookId = request.POST.get('id')
        data = {}
        if bookId:
            Book.objects.get(id=bookId).delete()
            data['success'] = 1
        else:
            data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self, *args, **kwargs):
        data = {}
        data = Book.objects.filter()

        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('books')
        return context


class BookCreateView(CreateView):
    form_class = BookForm
    template_name = 'book/form/create_form.html'
    success_url = 'books'

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url))

    def get_context_data(self, **kwargs):
        context = super(BookCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('add_book')
        context['form_title'] = '添加书籍'
        return context


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'book/form/create_form.html'
    form_class = BookForm
    success_url = 'books'

    def get_context_data(self, **kwargs):
        context = super(BookUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('edit_book', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑书籍'
        return context

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url))


class ChapterListView(ListView):
    template_name = 'book/chapter_list.html'
    context_object_name = "data"
    paginate_by = 100

    def post(self, request, **kwargs):
        id = request.POST.get('id')
        data = {}
        if id:
            Chapter.objects.get(id=id).delete()
            data['success'] = 1
        else:
            data['success'] = 0

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_queryset(self):
        book_id = self.kwargs.get('bid')
        listdata = {}
        if book_id:
            listdata = ChapterTreeUtil.getChapterList(book_id, 0, 0)

        if not book_id:
            raise Http404()

        return listdata

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChapterListView, self).get_context_data(**kwargs)
        context['book_id'] = self.kwargs.get('bid')
        context['form_url'] = reverse('chapters', kwargs={'bid': context['book_id']})
        context['q'] = self.request.GET.get('q', '')
        return context


class ChapterCreateView(CreateView):
    form_class = ChapterForm
    template_name = 'book/form/create_form.html'
    success_url = 'chapters'
    pid = 0

    def get_form_kwargs(self):
        kw = super(ChapterCreateView, self).get_form_kwargs()
        kw.update({
            'pid': self.pid,
            'book_id': self.kwargs.get('bid')
        })
        return kw

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'bid': self.kwargs.get('bid')}))

    def get_initial(self):
        initial = super(ChapterCreateView, self).get_initial()
        self.pid = self.request.GET.get('pid', 0)
        return initial

    def get_context_data(self, **kwargs):
        context = super(ChapterCreateView, self).get_context_data(**kwargs)
        context['book_id'] = self.kwargs.get('bid')
        context['form_url'] = reverse('add_chapter', kwargs={'bid': context['book_id']})
        context['form_title'] = '添加章节'
        return context


class ChapterUpdateView(UpdateView):
    model = Chapter
    template_name = 'book/form/create_form.html'
    form_class = ChapterForm
    success_url = 'chapters'

    def get_context_data(self, **kwargs):
        context = super(ChapterUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('edit_chapter', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        context['form_title'] = '编辑章节'
        return context

    def form_valid(self, form):
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse(self.success_url, kwargs={'bid': form.data.get('book_id')}))



