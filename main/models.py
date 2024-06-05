from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TodoList(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_lists"
    )
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="lists")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def modified_at(self):
        try:
            time = self.items.order_by("modified_at")[0].modified_at
        except:
            time = self.created_at
        return time

    @property
    def stats(self):
        x = self.items
        return f"Pending : {x.filter(status="P").count()} In-Progress: {x.filter(status="I").count()} Completed : {x.filter(status="C").count()}"
        


class TodoListItem(models.Model):
    STATUS_CHOICES = {"P": "Pending", "I": "In-Progress", "C": "Completed"}
    PRIORITY_CHOCIES = {"H" : "High", "M": "Medium", "L": "Low"}
    todo_list = models.ForeignKey(
        TodoList, on_delete=models.CASCADE, related_name="items"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOCIES, default="M")


class TodoInvitation(models.Model):
    STATUS_CHOICES = {"P": "Pending", "A": "Accepted", "R": "Rejected"}
    todo_list = models.ForeignKey(
        TodoList, on_delete=models.CASCADE, related_name="invites"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invites"
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
