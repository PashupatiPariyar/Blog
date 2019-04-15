from urllib.parse import quote_plus
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request): #List item
    queryset_list = Post.objects.active()#.order_by("-timestamp")
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
    page_request_var ="page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {
        'object_list': queryset,
        'title': 'List',
        'page_request_var': page_request_var,
    }
    # if request.user.is_authenticated:
    #     context = {
    #         'title': 'My User List'
    #     }
    # else:
    #     context = {
    #         'title': 'List'
    #     }
    return render(request, 'post/post_list.html', context)

def post_detail(request, id=None): #retrive
    # instance = Post.objects.get(id=id)
    instance = get_object_or_404(Post, id=id)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        'title': instance.title,
        'instance':instance,
        'share_string': share_string,
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)#form validation
    if form.is_valid(): #adding post
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        # messages.success(request,'Post has been successfully created', extra_tags='some-tag')
        return HttpResponseRedirect(instance.get_absolute_url())#redirect to its own page
    # else:
    #     messages.error(request, 'Post has not been created')

    context = {
        'form': form,
    }
    return render(request, 'post/post_form.html', context)


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #message success
        # messages.success(request, 'Post has been successfully edited')
        return HttpResponseRedirect(instance.get_absolute_url()) #redirect to its own page
    # else:
    #     messages.error(request, 'Post has not been edited')

    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'post/post_form.html', context)


def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Post has been successfully deleted')
    return redirect('post:list')

