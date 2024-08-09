from django.shortcuts import render, redirect, get_object_or_404 # redirect 함수는 다른 URL로 이동하는 함수
from .models import Task, List
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all().order_by('-created_date')
    list = List.objects.all()
    return render(request, 'todoapp/task_list.html', {'tasks': tasks, 'lists': list}) # task_list.html 템플릿을 렌더링한다.

def add_task(request):
    if request.method == 'POST': # 폼이 제출 되었을때 POST 요청을 처리한다. 처리가됨
        form = TaskForm(request.POST) # POST 요청으로 전달된 데이터를 사용해 TaskForm 인스턴스를 생성한다.
        if form.is_valid(): # form의 데이터가 유효한지 검사 -> 모델/제약조건을 기반으로 자동 유효성 검증을 수행한다.
            form.save() # form의 데이터를 데이터베이스에 저장한다.
            return redirect('task_list') # task_list 뷰로 이동한다.
    else:
        form = TaskForm() # GET 요청일때는 빈 TaskForm 인스턴스를 생성한다.
    lists = List.objects.all()
    return render(request, 'todoapp/add_task.html', {'form': form, 'lists':lists}) # 폼을 포함한 add_task.html 템플릿을 렌더링한다.

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