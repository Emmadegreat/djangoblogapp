from django import forms
from blogapp.models import  Category, Blogs, BlogUser
from django.contrib.auth.forms import UserCreationForm


class AddCategoryForm(forms.ModelForm):
    category_name = forms.CharField(
        max_length=50,
        label="Category Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style':'border-radius: 6px; width: 300px; height: 40px; padding:6px; border:1px solid #000',
        })
    )


    class Meta:
        model = Category
        fields= ('category_name',)

STATUS_CHOICES=[
    ('draft','draft'),
    ('published','published'),
]

class AddPostForm(forms.ModelForm):
    title = forms.CharField(label='title', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ModelChoiceField(label='category', queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    blog_image = forms.ImageField(label='blog_image')
    short_description = forms.CharField(label='short_description', widget=forms.Textarea())
    blog_body = forms.CharField(label='short_description', widget=forms.Textarea())
    status = forms.ChoiceField(label='status', choices=STATUS_CHOICES, widget=forms.Select)
    # is_featured = forms.BooleanField(label='is_featured', default=False)



    class Meta:
        model = Blogs
        fields = ('title', 'category', 'blog_image', 'short_description', 'blog_body', 'status', 'is_featured')


class AddUserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name= forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email= forms.CharField(label='Email', widget=forms.EmailInput())

    class Meta:
        model = BlogUser
        fields = ('first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'groups')