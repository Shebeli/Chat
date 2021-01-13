from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        a = getattr(obj, 'creator', None)
        b = getattr(obj, 'sender', None)
        c = getattr(obj, 'user1', None)
        d = getattr(obj, 'user2', None)
        if a is not None:
            return obj.creator == request.user
        elif b is not None:
            return obj.sender == request.user
        elif c is not None:
            return obj.user1 == request.user
        elif d is not None:
            return obj.user2 == request.user
        return False