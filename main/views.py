from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TodoInvitation, TodoList, TodoListItem

# Create your views here.
@login_required
def home(request):
    user = request.user

    lists = user.lists.all()
    return render(request, "main/home.html", {"lists": lists})

@login_required
def manage_list(request, list_id):
    try:
        todo_list = TodoList.objects.get(id=list_id)
    except TodoList.DoesNotExist:
        messages.error(request, "No such list exists")
        return redirect("main:home")
    if request.method == "GET":
            
        if request.user not in todo_list.members.all():
            messages.error(request, "You don't have access to this list")
            return redirect("main:home")

        context = {"list": todo_list, "owner":(request.user == todo_list.owner)}

        return render(request, "main/manage.html", context)
    if request.method == "POST":
       updated_keys = [int(k.split("_")[-1]) for k in request.POST.dict().keys() if "csrf" not in k and k.split("_")[-1].isdigit()]
       items = [i.id  for i in todo_list.items.all()]

       if updated_keys == items:
            for key in updated_keys:
               new_status=request.POST["status_select_" + str(key)]
               if new_status != todo_list.items.get(id=key):
                   item = todo_list.items.get(id=key)
                   item.status = new_status
                   item.save()
            messages.success(request, "Updated Successfully!")
            return redirect("main:manage", list_id=list_id)
       else:
           messages.error(request,"Invalid Request!")
           return redirect("main:manage", list_id=list_id)


@login_required
def create_list(request):
    if request.method =="POST":
        name = request.POST["name"]
        owner = request.user
        try:
            created_list = TodoList.objects.create(owner=owner, name=name)
            created_list.members.add(owner)
            messages.success(request, "Created List Successfully!")
            return redirect("main:manage", list_id=created_list.id)
        except:
            messages.error(request,"Failed to create list")
            return redirect("main:create_list")
    return render(request, "main/create_list.html")

@login_required
def create_item(request, list_id):
    try:
        todo_list = TodoList.objects.get(id=list_id)
    except TodoList.DoesNotExist:
        messages.error(request, "No such list exists")
        return redirect("main:home")
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        priority = request.POST["priority"]
        TodoListItem.objects.create(todo_list = todo_list,title=title,description=description, priority=priority,created_by=request.user)
        return redirect("main:manage", list_id=list_id)
    return render(request, "main/create_item.html")

@login_required
def invite_members(request, list_id):
    try:
        todo_list = TodoList.objects.get(id=list_id)
    except TodoList.DoesNotExist:
        messages.error(request, "No such list exists")
        return redirect("main:home")

    if not todo_list.owner == request.user:
        messages.error(request, "You don't have access to this page")
        return redirect("main:home")

    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["username"])

            if user in todo_list.members.all():
                messages.error(request, "User is already a member")
                return redirect("main:invite_members", list_id=list_id)

            if TodoInvitation.objects.filter(recipient=user).exists():
                messages.error(request, "User already invited")
                return redirect("main:invite_members", list_id=list_id)

            TodoInvitation.objects.create(todo_list = todo_list, recipient=user)

            messages.success(request,"User Invited!")
            return redirect("main:invite_members", list_id=list_id)

        except User.DoesNotExist:
            messages.error(request, "No Such User exists")
            return redirect("main:invite_members", list_id=list_id)


    return render(request, "main/invite_members.html")

@login_required
def manage_members(request, list_id):
    try:
        todo_list = TodoList.objects.get(id=list_id)
    except TodoList.DoesNotExist:
        messages.error(request, "No such list exists")
        return redirect("main:home")
    if todo_list.owner != request.user:
        messages.error(request, "You don't have access to this")
        return redirect("main:home")


    members = [{"username": member.username, "items": member.todolistitem_set.filter(todo_list=todo_list)} for member in todo_list.members.exclude(id = request.user.id)]

    return render(request, "main/manage_members.html", {"members": members, "list": todo_list})

@login_required
def revoke_access(request,list_id, username ):
    try:
        todo_list = TodoList.objects.get(id=list_id)
        user = User.objects.get(username=username)
    except TodoList.DoesNotExist:
        messages.error(request, "No such list exists")
        return redirect("main:home")
    except User.DoesNotExist:
        messages.error(request, "No such user exists")
        return redirect("main:home")
    if todo_list.owner == user:
        messages.error(request, "Cannot remove owner from todolist")
        return redirect("main:home")

    if todo_list.owner != request.user:
        messages.error(request, "You don't have access to this")
        return redirect("main:home")

    if not todo_list.members.filter(id = user.id).exists():
        messages.error(request, "User is not part of todolist")
        return redirect("main:home")

    todo_list.members.remove(user)
    messages.success(request, "Removed user!")
    return redirect("main:manage", list_id)



@login_required
def show_invites(request):
    invites = TodoInvitation.objects.filter(recipient=request.user, status="P")

    return render(request, "main/show_invites.html", {"invites" : invites})

@login_required
def accept_invite(request, invite_id):
    try:
        invite= TodoInvitation.objects.get(id=invite_id)
    except TodoInvitation.DoesNotExist:
        messages.error(request, "No such invite exists")
        return redirect("main:show_invites")
    if not invite.recipient == request.user:
        messages.error(request, "You don't have access to this")
        return redirect("main:show_invites")

    invite.todo_list.members.add(request.user)
    invite.status = "A"
    invite.save()
    messages.success(request, "Accepted Invite to {}".format(invite.todo_list.name))
    return redirect("main:home")

@login_required
def decline_invite(request, invite_id):
    try:
        invite= TodoInvitation.objects.get(id=invite_id)
    except TodoInvitation.DoesNotExist:
        messages.error(request, "No such invite exists")
        return redirect("main:show_invites")
    if not invite.recipient == request.user:
        messages.error(request, "You don't have access to this")
        return redirect("main:show_invites")

    invite.status = "D"
    invite.save()
    messages.success(request, "Declined Invite to {}".format(invite.todo_list.name))
    return redirect("main:home")

