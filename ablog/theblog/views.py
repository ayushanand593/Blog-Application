from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Person, User
from .forms import PostForm, EditForm, CommentForm, SearchForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .resources import PersonResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



# def home(request):
#  return render(request,'home.html' , {})
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']

    # ordering=['-id']
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html',
                  {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'


class AddCategoryView(CreateView):
    model = Category
    fields = '__all__'
    template_name = 'add_category.html'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'


#  fields=['title','title_tag','body']
class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    # fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('home')

from django.shortcuts import render
from django.contrib import messages
from tablib import Dataset
from .resources import PersonResource
from .models import Person

def simple_upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        myfile = request.FILES.get('myfile', None)
        if myfile is None:
            messages.error(request, 'No file uploaded.')
            return render(request, 'upload.html')
        elif not myfile.name.endswith('xlsx'):
            messages.error(request, 'Wrong file format. Only .xlsx files are allowed.')
            return render(request, 'upload.html')
        imported_data = dataset.load(myfile.read(), format='xlsx')
        for data in imported_data:
            value = Person(
                data[0],
                data[1],
                data[2],
                data[3]
            )
            value.save()
        
    return render(request,'upload.html')

from django.shortcuts import render
from django.contrib.auth.models import User

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            username = form.cleaned_data['username']
            users = User.objects.filter(username__icontains=username)
            return render(request, 'search_results.html', {'users': users})
    else:
        form = SearchForm()
    return render(request, 'search_form.html', {'form': form})

'''def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            results = User.objects.filter(username__icontains=query)
            return render(request, 'search_results.html', {'results': results})
    return render(request, 'search_results.html')'''

def index(request):
    return render(request, 'index.html')






