from django import forms


class PsychicForm(forms.Form):
    answer = forms.IntegerField(min_value=10, max_value=99, required=False)


