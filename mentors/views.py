from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.

class MentorListView(ListView):
#referred from boards.views.TopicListView
    model = User
    context_object_name = 'users'
    template_name = 'mentors.html'
    paginate_by = 5