from django.urls import path
from .views import create_list, home, invite_members,manage_list,create_item, revoke_access,show_invites,accept_invite,decline_invite,manage_members

app_name = "main"

urlpatterns = [
        path("", home, name="home"),
        path("manage/<int:list_id>", manage_list, name="manage"),
        path("invites/", show_invites, name="show_invites"),
        path("invites/<int:invite_id>/accept", accept_invite, name="accept_invite"),
        path("invites/<int:invite_id>/decline", decline_invite,name="decline_invite"),
        path("list/create/", create_list, name="create_list"),
        path("list/<int:list_id>/create_item", create_item, name="create_item"),
        path("list/<int:list_id>/invite_members", invite_members, name="invite_members"),
        path("list/<int:list_id>/members", manage_members, name="manage_members"),
        path("list/<int:list_id>/members/<str:username>/revoke", revoke_access, name="revoke_access")
    ]
