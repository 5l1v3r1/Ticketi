from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Ticket

class IsOwnerOrReadOnly(BasePermission): #TODO: edit
    my_safe_method = ['GET', 'PUT']
    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, ticket):
        return request.user in ticket.contributers.all()

class IsInListContributers(BasePermission):
    my_safe_method = ['GET', 'PATCH'] #TODO: remove 'GET' for production
    def has_permission(self, request, view):

        # check request method
        if not request.method in self.my_safe_method:
            return False

        # check object permission
        ticket_id = view.kwargs.get('pk', None)

        if not ticket_id:
            return False

        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            return False

        if request.user in ticket.in_list_contributers.all():
            return True

        return False

class LikeOwner(BasePermission):
    my_safe_method = ['DELETE']
    def has_permission(self, request, view):

        # check request method
        if not request.method in self.my_safe_method:
            return False

        # check object permission
        ticket_id = view.kwargs.get('pk', None)

        if not ticket_id:
            return False

        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            return False

        if request.user in ticket.in_list_contributers.all():
            return True

        return False
