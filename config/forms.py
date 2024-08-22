from django import forms
from .models import Task, List

class TaskForm(forms.ModelForm):
    list = forms.ModelChoiceField(queryset=List.objects.all(), empty_label=None)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'list']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } # due_date 필드에 대한 위젯을 지정
