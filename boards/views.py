from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView
from django.utils import timezone

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView): #UpdateView is one of the generic class-based views (other view types: class-based view, function-based view)
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk' # pk_url_kwarg = identify the name of the keyword argument used to retrieve the Post object. It’s the same as we define in the urls.py.
    context_object_name = 'post' # if context_object_name is not set, it will be available in the template as “object”
	
    def get_queryset(self):
        queryset = super().get_queryset() # reusing the get_queryset method from the parent class, that is, the UpateView class
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

class BoardListView(ListView): # the equivalent of home (function-based view)
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

def board_topics(request, pk):
    # try:
	    # board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
        # raise Http404
    # return render(request, 'topics.html', {'board': board})
	
    # board = get_object_or_404(Board, pk=pk)
    # topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    # return render(request, 'topics.html', {'board': board, 'topics': topics})

    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics.html', {'board': board, 'topics': topics})	

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

@login_required #it means that this method only can be accessed by logged-in users. If the user's not logged in, he/she will be redirected to login page
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    #user = User.objects.first()  # just picking the first user from the User table

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False) #by default, commit = True and save is executed automatically afterwards. But since board and starter the values are non-nullable, it will create an exception. Therefore, save() is called manually at the end after we provide the board and starter values
            topic.board = board
            topic.starter = request.user #takes the logged in user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by = request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

@login_required	
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk) 
        if not self.request.session.get(session_key, False): # so that if the same user refreshing the page, the view count is not increased
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()
			
            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
            # return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
            # return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})