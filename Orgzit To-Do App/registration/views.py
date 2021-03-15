from django.shortcuts import render
from registration.models import Registration
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

# Create your views here.
def land_redirect(request):

    return render(request, 'index.html')

def create(request):

    return render(request, 'create.html')

def read(request):

    todos = Registration.objects.all().values()
    for todo in todos:
        if todo['status']==1:
            todo['status'] = "Pending"

        elif todo['status']==2:
            todo['status'] = "In Progress"

        else:
            todo['status'] = "Completed"

    args= {'data': todos}

    return render(request, 'read.html',args)

def update_delete(request):

    todos = Registration.objects.all().values()
    for todo in todos:
        if todo['status']==1:
            todo['status'] = "Pending"

        elif todo['status']==2:
            todo['status'] = "In Progress"

        else:
            todo['status'] = "Completed"

    args= {'data': todos}

    return render(request, 'update.html',args)


def save(request):
    if request.method == 'POST':
        feed = Registration()
        print(request.POST.get('status'))
        if request.POST.get('title') and request.POST.get('email') and request.POST.get('password'):

            feed.title = request.POST.get('title')
            feed.email = request.POST.get('email')
            feed.description = request.POST.get('description')
            feed.password = make_password(request.POST.get('password'))
            feed.status = request.POST.get('status')
            feed.time = request.POST.get('time')

            feed.save()

            messages.success(request, 'To-do created successfully')
            args = {'message': messages}

    return render(request, 'create.html',args)

def updatedb(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        feed = Registration.objects.get(email=email)
        if request.POST.get("update"):

            if request.POST.get('title') and request.POST.get('email'):

                if request.POST.get('status') == None:
                    feed.status = feed.status
                else:
                    feed.status = request.POST.get('status')

                if request.POST.get('time') =="":
                    feed.time = feed.time
                else:
                    feed.time = request.POST.get('time')

                feed.title = request.POST.get('title')
                feed.description = request.POST.get('description')

                feed.save()

                messages.success(request, 'To-do updated successfully')


        elif request.POST.get("delete") :

            feed.delete()
            messages.success(request, 'To-do deleted successfully')


        args = {'message': messages}
    return HttpResponseRedirect('/todo/update_delete/', args)


class ReadTodo(ListView):
    template_name = 'registration_list.html'
    model = Registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for todo in context['object_list']:
            print(todo.email)
            if todo.status == 1:
                todo.status = "Pending"

            elif todo.status == 2:
                todo.status = "In Progress"

            else:
                todo.status = "Completed"

        return context
