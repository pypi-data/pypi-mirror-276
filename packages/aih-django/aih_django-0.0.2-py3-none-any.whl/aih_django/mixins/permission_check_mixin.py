
# allows from rest_framework.decorators import permission_classes to be used on class based views
class PermissionDecoratorMixin:
    def get_permissions(self):
        # Check if the action has custom permission classes
        action = getattr(self, self.action, None)
        if action and hasattr(action, "permission_classes"):
            permission_classes = action.permission_classes
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]
