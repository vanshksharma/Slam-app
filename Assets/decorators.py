from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import Asset


def auth_asset(func):
    @wraps(func)
    def wrapper(self, request, user_dict, *args, **kwargs):
        asset_id = request.data.get('asset', None)
        if not asset_id:
            return Response({'Error': 'No Asset ID provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            asset = Asset.objects.select_related('project').get(id=asset_id)
        except (Asset.DoesNotExist, ValueError):
            return Response({'Error': "Please Enter Valid Asset ID"},
                            status=status.HTTP_400_BAD_REQUEST)

        if asset.user.id != user_dict['id']:
            return Response({'Error': "The Asset does not belong to the user"},
                            status=status.HTTP_403_FORBIDDEN)

        return func(self, request, user_dict, asset, *args, **kwargs)

    return wrapper