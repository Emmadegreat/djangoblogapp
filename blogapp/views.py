from django.shortcuts import render, redirect,get_object_or_404
from . models import Blogs, Category, BlogUser, Comment, ContactUs, NewsLetter
from django.db.models import Q, Prefetch
from django.contrib.auth import authenticate, login as auth_login, logout
from blogapp.form import RegisterForm, LoginForm, ContactUsForm, SubscribeForm, UnSubscribeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.conf import settings
import os
from django.contrib.auth.models import Group
from django.core.mail import send_mail, send_mass_mail
from . decorator import allowed_users, admin_only
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


def home(request):
    categories = Category.objects.all()
    featured_post = Blogs.objects.filter(is_featured=True, status="published")
    posts = Blogs.objects.filter(is_featured=False, status="published")


    context = {
        'categories': categories,
        'featured_post': featured_post,
        'posts': posts,
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


def post_by_category(request, category_id):

    posts = Blogs.objects.filter(status="published", category=category_id)

    try:
       category = Category.objects.get(pk=category_id)
    except:
        return redirect('home')

    category = get_object_or_404(Category, pk=category_id)

    context = {
        "posts": posts,
        "category": category
    }
    return render(request, "post_by_category.html", context)



COMMENT_MAX_LENGTH = 1000
COMMENT_COOLDOWN_SECONDS = 20

def single_blog(request, slug):
    blog_details = get_object_or_404(Blogs, slug=slug, status="published")

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to comment.")
            return redirect(f"{reverse('login')}?next={request.path}%23comments")

        text = request.POST.get('comment', '').strip()

        if not text:
            messages.error(request, "Please write a comment before submitting.")
        elif len(text) > COMMENT_MAX_LENGTH:
            messages.error(request, f"Comments can be at most {COMMENT_MAX_LENGTH} characters.")
        else:
            too_soon = Comment.objects.filter(
                author=request.user,
                created_at__gte=timezone.now() - timedelta(seconds=COMMENT_COOLDOWN_SECONDS),
            ).exists()
            duplicate = Comment.objects.filter(
                author=request.user, post=blog_details, comment=text
            ).exists()

            if too_soon:
                messages.error(request, "You're commenting too fast. Please wait a few seconds.")
            elif duplicate:
                messages.info(request, "You've already posted this comment.")
            else:
                Comment.objects.create(author=request.user, post=blog_details, comment=text)
                messages.success(request, "Your comment has been posted.")

        return HttpResponseRedirect(f"{request.path}#comments")

    comments = (
        Comment.objects.filter(post=blog_details, parent__isnull=True)
        .select_related('author')
        .prefetch_related(Prefetch(
            'replies',
            queryset=Comment.objects.select_related('author').order_by('created_at'),
        ))
    )
    context = {
        "blog_details": blog_details,
        "comments": comments,
        "comment_count": Comment.objects.filter(post=blog_details).count(),
    }
    return render(request, "single_blog_page.html", context)



def _login_redirect(request, comment):
    messages.error(request, "Please log in first.")
    return redirect(f"{reverse('login')}?next={comment.post.get_absolute_url()}%23comments")


@require_POST
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_url = f"{comment.post.get_absolute_url()}#comments"

    if not request.user.is_authenticated:
        return _login_redirect(request, comment)

    if comment.author_id != request.user.id:          # only the author may edit
        messages.error(request, "You can only edit your own comments.")
        return HttpResponseRedirect(post_url)

    text = request.POST.get('comment', '').strip()
    if not text:
        messages.error(request, "A comment can't be empty.")
    elif len(text) > COMMENT_MAX_LENGTH:
        messages.error(request, f"Comments can be at most {COMMENT_MAX_LENGTH} characters.")
    elif text == comment.comment:
        messages.info(request, "No changes were made.")
    else:
        comment.comment = text
        comment.save()
        messages.success(request, "Your comment has been updated.")
    return HttpResponseRedirect(post_url)


@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_url = f"{comment.post.get_absolute_url()}#comments"

    if not request.user.is_authenticated:
        return _login_redirect(request, comment)

    if comment.author_id != request.user.id and not request.user.is_staff:
        messages.error(request, "You can't delete this comment.")
        return HttpResponseRedirect(post_url)

    comment.delete()
    messages.success(request, "Comment deleted.")
    return HttpResponseRedirect(post_url)



@require_POST
def reply_comment(request, comment_id):
    target = get_object_or_404(Comment, pk=comment_id)
    top = target.parent or target                      # keep replies one level deep
    post_url = top.post.get_absolute_url()

    if not request.user.is_authenticated:
        return _login_redirect(request, top)

    text = request.POST.get('comment', '').strip()
    if not text:
        messages.error(request, "A reply can't be empty.")
    elif len(text) > COMMENT_MAX_LENGTH:
        messages.error(request, f"Replies can be at most {COMMENT_MAX_LENGTH} characters.")
    else:
        too_soon = Comment.objects.filter(
            author=request.user,
            created_at__gte=timezone.now() - timedelta(seconds=COMMENT_COOLDOWN_SECONDS),
        ).exists()
        duplicate = Comment.objects.filter(
            author=request.user, post=top.post, comment=text
        ).exists()

        if too_soon:
            messages.error(request, "You're commenting too fast. Please wait a few seconds.")
        elif duplicate:
            messages.info(request, "You've already posted this.")
        else:
            Comment.objects.create(author=request.user, post=top.post, parent=top, comment=text)
            messages.success(request, "Your reply has been posted.")

    return HttpResponseRedirect(f"{post_url}#comment-{top.id}")



def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blogs.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status="published")
    context = {
        "keyword": keyword,
        "blogs": blogs
    }
    return render(request, "search.html", context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        form = RegisterForm()

        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                user = form.save()
                user.is_staff = False
                first_name = form.cleaned_data.get('first_name')

                custom_users, created = Group.objects.get_or_create(name="custom_users")
                user.groups.add(custom_users)

                messages.success(request, f"Welcome {first_name}, you have successfully registered. You can proceed to login")
                return redirect('login')

        else:
            form = RegisterForm()

        return render(request, 'register.html', {'form':form})

def Logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')


# def login(request):
#     if request.user.is_authenticated:
#         return redirect('home')


#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 auth_login(request, user)
#                 messages.success(request, f"You have been logged in as {user.first_name}")
#                 return redirect('home')

#     return render(request, 'login.html', {'form': form})



def login(request):
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    if not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        next_url = ''          # ignore unsafe redirects to other sites

    if request.user.is_authenticated:
        return redirect(next_url or 'home')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, f"You have been logged in as {user.first_name}")
                return redirect(next_url or 'home')

            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html', {'form': form, 'next': next_url})


def contact_us_view(request):
    #form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save()

            subject = f"New contact us mail from {contact.fullname}"
            message = f"""
                        You have received a new mail from your website contact us page:
                        Full Name: {contact.fullname}
                        Email: {contact.email}
                        Phone: {contact.phone}
                        message: {contact.message}
                        """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.ADMIN_EMAIL]

            try:
                send_mail(subject, message,from_email,recipient_list)
                messages.success(request, 'Your email has been sent successfully')

            except Exception as e:
                messages.error(request, 'An error has occurred while sending your email')

            return render(request, 'contact_us.html', {'form': ContactUsForm()})

    form = ContactUsForm()

    return render(request, 'contact_us.html', {'form': form})



@admin_only
def contact_us_data_view(request):
    contact_data = ContactUs.objects.all()
    return render(request, 'dashboard/contact_us_data.html', {'contact_data': contact_data})

@admin_only
def newsletter_view(request):
    newsletter_data = NewsLetter.objects.all()
    return render(request, 'dashboard/newsletter.html', {'newsletter_data': newsletter_data})


def not_allowed(request):
    return render(request, 'not_allowed.html')


#======newsletter
def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = NewsLetter.objects.get_or_create(email=email)

            if not created:
                if subscriber.subscribed:
                    return JsonResponse({'success': False, 'error': "You're already subscribed."}, status=400)
                else:
                    subscriber.subscribed = True
                    subscriber.save()

                    send_mail( #send notification mail to the subscriber
                        'subscription successful',
                        'You have successfully re-subscribed to our newsletter',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )

                    send_mail( #send notification mail to the admin
                        'New mail re-subscription',
                        f"The mail {email} has re-subscribed to the newsletter",
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )

                    return JsonResponse({'success': True, 'message': "You've successfully re-subscribed!"})
            else:

                send_mail( #send notification mail to the subscriber
                    "Subscription success",
                    "Thank you for subscribing to our newsletter",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                send_mail( #send notification mail to the admin
                    "New subscription Notice",
                    f"The user with email {email} has subscribed to our newsletter",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )

                return JsonResponse({'success': True, 'message': "You've successfully subscribed!"})
        else:
            return JsonResponse({'success': False, 'error': "Invalid input."}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)




def unsubscribe(request):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                subscriber = NewsLetter.objects.get(email=email)
                if subscriber.subscribed:
                    subscriber.subscribed = False
                    subscriber.save()
                    messages.success(request, 'You have successfully unsubscribed from this newsletter')

                else:
                    messages.info(request, 'You are not currently subscribed to this newsletter')

            except NewsLetter.DoesNotExist:
                messages.error(request, 'Email not found')

            return redirect('dashboard')

    else:
        form = UnSubscribeForm()

    return render(request, 'subscribe.html', {'form': form})



def bad_request(request, exception):

    return render(request, '400.html', status=400)# trying to make unexpected request or POST/GET method that is not correct

def permission_denied(request, exception): #permission like login related error

    return render(request, '403.html', status=403)

def page_not_found(request, exception):

    return render(request, '404.html', status=404) #trying to access a page that is not existing in the website

def server_error(request):

    return render(request, '500.html', status=500)# server error like wrong configuration of data/details


#Google verification route for google console and ranking
def google_verification(request):
    file_path = os.path.join(settings.STATIC_ROOT, "google1fc99727dbd27deb.html")
    with open(file_path, "r") as file:
        return HttpResponse(file.read(), content_type="text/html")