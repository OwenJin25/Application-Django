from django.shortcuts import render
from .models import Topic, Comment
from django.shortcuts import redirect
from .forms import TopicForm, CommentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def topic_list(request):
    topics = Topic.objects.all()  # Recupera todos os tópicos do banco de dados
    return render(request, 'topics/topic_list.html', {'topics': topics})

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)  # Busca o tópico ou retorna 404
    comments = topic.comments.all()  # Recupera todos os comentários do tópico
    return render(request, 'topics/topic_detail.html', {'topic': topic, 'comments': comments})

@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user  # Define o autor como o usuário atual
            topic.save()
            return redirect('topic_list')
    else:
        form = TopicForm()
    return render(request, 'topics/create_topic.html', {'form': form})

@login_required
def add_comment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = CommentForm()
    return render(request, 'topics/add_comment.html', {'form': form, 'topic': topic})

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'topics/edit_topic.html', {'form': form, 'topic': topic})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        topic.delete()
        return redirect('topic_list')
    return render(request, 'topics/delete_topic.html', {'topic': topic})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=comment.topic.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'topics/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden() 
    if request.method == 'POST':
        topic_id = comment.topic.id  
        comment.delete()
        return redirect('topic_detail', topic_id=topic_id)
    return render(request, 'topics/delete_comment.html', {'comment': comment})

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user != topic.author:
        return redirect('topic_detail', topic_id=topic_id)  # Usuário não autorizado

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)

    return render(request, 'topics/edit_topic.html', {'form': form, 'topic': topic})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        # Deletar o tópico
        topic.delete()
        return redirect('topic_list')  # Redireciona para a lista de tópicos

    return render(request, 'topics/delete_topic.html', {'topic': topic})
