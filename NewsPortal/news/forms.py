from django import forms
from .models import Post, Author


class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.select_related('user'),
        empty_label='Автор не выбран',
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'post_type',
            'category'
        ]