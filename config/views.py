from django.shortcuts import render, redirect, get_object_or_404 # redirect 함수는 다른 URL로 이동하는 함수
from .models import Task, List
from .forms import TaskForm
from django.db.models import Count

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

def set_priority(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        priority = request.POST.get('priority')
        if priority in ['1','2','3']:
            task.priority = int(priority)
            task.save()
    return redirect('task_list') # task_list 뷰로 리다이렉트한다.

def task_statistics(request): # 전체 추가
    tasks = Task.objects.all()

    # 통계 계산
    statistics = {
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(completed=True).count(),
        'incomplete_tasks': tasks.filter(completed=False).count(),
        'high_priority_tasks': tasks.filter(priority=3).count(),
        'medium_priority_tasks': tasks.filter(priority=2).count(),
        'low_priority_tasks': tasks.filter(priority=1).count(),
    }

    # 우선순위별 완료율 계산
    for priority in [1, 2, 3]:
        priority_tasks = tasks.filter(priority=priority)
        total = priority_tasks.count()
        completed = priority_tasks.filter(completed=True).count()
        statistics[f'priority_{priority}_completion_rate'] = (completed / total * 100 if total > 0 else 0)

    return render(request, 'todoapp/task_statistics.html', {'statistics': statistics})