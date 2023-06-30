from typing import Any, Dict
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from .models import Post,Comment
from  django.urls import reverse_lazy
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

    

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
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

