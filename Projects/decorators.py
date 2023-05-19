from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Project


def auth_project(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        project_id = request.data.get('project', None)
        if not project_id:
            return Response({'Error': 'No Project ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.select_related('lead').get(id=project_id)
        except Project.DoesNotExist:
            return Response({'Error': "Please Enter Valid Project ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if project.lead.customer.user.id != user_dict['id']:
            return Response({'Error': "The project does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, project, *args, **kwargs)

    return wrapper