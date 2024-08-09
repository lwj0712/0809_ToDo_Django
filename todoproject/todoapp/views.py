from django.shortcuts import render, redirect, get_object_or_404 # redirect 함수는 다른 URL로 이동하는 함수
from .models import Task, List
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all().order_by('-created_date')
    lists = List.objects.all()
    return render(request, 'todoapp/task_list.html', {'tasks': tasks, 'lists': lists}) # task_list.html 템플릿을 렌더링한다.

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    lists = List.objects.all()
    return render(request, 'todoapp/add_task.html', {'form': form, 'lists': lists})



def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todoapp/edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todoapp/delete_task.html', {'task': task})