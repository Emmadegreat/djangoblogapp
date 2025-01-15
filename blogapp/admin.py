from django.contrib import admin
from .models import Category, Blogs, BlogUser, Comment, ContactUs, NewsLetter
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class BlogUserAdmin(UserAdmin):
    #model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name','created_at','updated_at')
    ordering = ['id']

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'category', 'author', 'blog_image', 'is_featured','status', 'created_at','updated_at')
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('id', 'title', 'status', 'category__category_name')
    list_editable = ('is_featured',)

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'comment_body', 'author', 'post', 'created_at', 'updated_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blogs, BlogAdmin)
admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Comment)
admin.site.register(ContactUs)
admin.site.register(NewsLetter)
## my user/password: Admin/Admin123.