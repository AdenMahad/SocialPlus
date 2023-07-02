from typing import Any, Dict
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView,ListView
from .models import Post,Comment,LikeDislike
from  django.urls import reverse_lazy,reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from SocialPlusApp.forms import CommentForm

# Create your views here.


# @method_decorator(login_required,name="dispatch")
class BlogListView(ListView):

    model = Post
    template_name = 'home.html'
    
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
    
def like_dislike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        like_dislike = LikeDislike.objects.filter(user=request.user, post=post).first()
        if 'like' in request.POST:
            if like_dislike:
                like_dislike.value = 1
                like_dislike.save()
            else:
                LikeDislike.objects.create(user=request.user, post=post, value=1)
        elif 'dislike' in request.POST:
            if like_dislike:
                like_dislike.value = -1
                like_dislike.save()
            else:
                LikeDislike.objects.create(user=request.user, post=post, value=-1)
    return redirect('home')




class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        post = self.get_object()
        num_likes = LikeDislike.objects.filter(post=post, value=1).count()
        num_dislikes = LikeDislike.objects.filter(post=post, value=-1).count()
        context['num_likes'] = num_likes
        context['num_dislikes'] = num_dislikes
        return context

class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields =['title','author','body']

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields =['title','body']

class BlogDeleteView(DeleteView): # new
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
def search(request):
    query = request.GET.get('q')
    if  Post.objects.filter(title__iexact=query):
        result = Post.objects.get(title=query)
        return render(request,"results.html",{"result":result})
    else:
       recommended = Post.objects.filter(title__icontains=query)
       return render(request,"recommended_entries.html",{"recommendations":recommended})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            pass
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')