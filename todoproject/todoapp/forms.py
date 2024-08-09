from django import forms
from .models import Task, List

class TaskForm(forms.ModelForm):
    list = forms.ModelChoiceField(queryset=List.objects.all(), required=False)

    class Meta:
        model = Task # task 모델과 해당 폼을 연결
        fields = ['title', 'description', 'due_date', 'list'] # 폼에 포함될 모델 필드를 지정
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } # due_date 필드에 대한 위젯을 지정
