from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from psychics.components.controller import Controller
from .forms import PsychicForm


class PsychicsView(View):
    def get_context(self, controller):
        return {
            'controller': controller,
            'guessed': controller.check_guess_answered()
        }

    @Controller.check_controller_exists
    def get(self, request: HttpRequest) -> HttpResponse:
        controller = Controller.get_from_session(request)
        context = self.get_context(controller)
        return render(request, 'index.html', context=context)
    
    @Controller.check_controller_exists
    def post(self, request: HttpRequest) -> HttpResponse:
        form = PsychicForm(request.POST)
        controller = Controller.get_from_session(request)
        
        if form.is_valid():
            if form.cleaned_data['answer'] is not None:
                controller.save_answer(form.cleaned_data['answer'])
            else:
                controller.make_guess()
        
        controller.save_to_session(request)
        
        context = self.get_context(controller)
        return render (request, 'index.html', context=context)
