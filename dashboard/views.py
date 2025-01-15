from django.shortcuts import render, redirect, get_object_or_404
from blogapp.models import Blogs, Category, BlogUser
from blogapp.decorator import allowed_users, admin_only
from django.contrib.auth.decorators import login_required, user_passes_test
from . form import AddCategoryForm, AddPostForm, AddUserForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group
# Create your views here.

@login_required(login_url="login")
@admin_only
def dashboard(request):
    blog_count = Blogs.objects.all().count()
    category_count = Category.objects.all().count()

    context = {
        "blog_count": blog_count,
        "category_count": category_count
    }
    return render(request,'dashboard/dashboard.html', context)


# def dashboard_redirect(request):
#     if request.user.is_superuser or request.user.groups.filter(name__in=["editors","managers"]).exists():
#         return redirect('dashboard')

#     else:
#         return redirect("home")


@login_required(login_url="login")
@allowed_users(allowed_roles=['editors'])
def categories(request):
    return render(request,'dashboard/categories.html')

@login_required(login_url="login")
@allowed_users(allowed_roles=['editors'])
def add_category(request):
    form = AddCategoryForm()

    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            category_name = form.cleaned_data['category_name']
            messages.success(request, f'you have added {category_name} as a new category')
            return redirect('categories')

    else:
        form = AddCategoryForm()

    return render(request,'dashboard/add_category.html', {'form': form})

@login_required(login_url='/login')
@allowed_users(allowed_roles=['editors'])
def edit_category(request,pk):

    if request.method == 'POST':
        category = Category.objects.get(pk=pk)
        form = AddCategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, 'category was successfully updated.')
            return redirect('categories')

    category = Category.objects.get(pk=pk)
    form = AddCategoryForm(instance=category)


    return render(request,'dashboard/edit_category.html', {'form': form})


@login_required(login_url='/login')
@allowed_users(allowed_roles=['editors'])
def delete_category(request,pk):

    category = Category.objects.get(pk=pk)
    category.delete()

    messages.error(request, 'category deleted')
    return redirect('categories')


#=====post functions=========
@login_required(login_url="login")
@allowed_users(allowed_roles=['editors'])
def posts(request):
    posts = Blogs.objects.all()
    return render(request,'dashboard/posts.html', {'posts': posts})

@login_required(login_url="login")
@allowed_users(allowed_roles=['editors'])
def add_post(request):
    form = AddPostForm()

    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()
            messages.success(request, f"You have successfully added new post with the title {title}")
            return redirect('posts')

    else:
        form = AddPostForm()
    return render(request,'dashboard/add_post.html', {'form': form})

@login_required(login_url='/login')
@allowed_users(allowed_roles=['editors'])
def edit_post(request,pk):

    if request.method == 'POST':
        edit_posts = Blogs.objects.get(pk=pk)
        form = AddPostForm(request.POST, instance=edit_posts)

        if form.is_valid():
            form.save()

            title = form.cleaned_data['title']
            messages.success(request, f"post with title {title} has been updated")
            return redirect('posts')

    edit_posts = Blogs.objects.get(pk=pk)
    form = AddPostForm(instance=edit_posts)


    return render(request,'dashboard/edit_post.html', {'form': form})

@login_required(login_url='/login')
@allowed_users(allowed_roles=['editors'])
def delete_post(request,pk):
    posts = Blogs.objects.get(pk=pk)
    posts.delete()

    messages.error(request, 'Woops! post deleted')
    return redirect('posts')


#users functions
@login_required(login_url='/login')
@user_passes_test(lambda user: user.is_superuser, login_url="/login")
def users(request):
    users = BlogUser.objects.all()

    return render(request, 'dashboard/users.html', {'users': users})


@login_required(login_url="/login")
@user_passes_test(lambda user: user.is_superuser, login_url="/login")
def add_user(request):
    form = AddUserForm()

    if request.method == 'POST':
        form = AddUserForm(request.POST)

        if form.is_valid():
            form.save()
            first_name = form.cleaned_data['first_name']

            messages.success(request, f"{first_name} has been added as a new user")
            return redirect('users')

    else:
        form = AddUserForm()

    return render(request,'dashboard/add_user.html', {'form': form})


@login_required(login_url='/login')
@user_passes_test(lambda user: user.is_superuser, login_url="/login")
def edit_user(request,pk):

    if request.method == 'POST':
        edit_user = BlogUser.objects.get(pk=pk)
        form = AddUserForm(request.POST, instance=edit_user)

        if form.is_valid():
            form.save()
            first_name = form.cleaned_data['first_name']
            messages.success(request, f"You have updated {first_name}'s data")
            return redirect('users')

    edit_user = BlogUser.objects.get(pk=pk)
    form = AddUserForm(instance=edit_user)

    return render(request, 'dashboard/edit_user.html', {'form':form})


@login_required(login_url='/login')
@user_passes_test(lambda user: user.is_superuser, login_url="/login")
def delete_user(request,pk):
    user = BlogUser.objects.get(pk=pk)
    user.delete()

    messages.error(request, 'Woops! you have deleted a user')
    return redirect('users')