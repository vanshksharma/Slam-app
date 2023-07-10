from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Asset
from django.conf import settings
from Auth.decorators import auth_user
from .serializers import AssetSerializer
from django.utils.text import get_valid_filename
from datetime import date,datetime
from Projects.models import Project
from django.db.models import Q
from .decorators import auth_asset
from .utils import upload_to_s3, delete_from_s3


class AssetHandler(APIView):
    @auth_user
    def get(self, request, user_dict):
        project_id = request.query_params.get('project', None) #Project Wise Asset GET
        if project_id:
            try:
                project = Project.objects.select_related('contact').get(id=project_id)
                if project.contact.user.id != user_dict['id']:
                    return Response({'Error': "The project does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
                
                assets=Asset.objects.select_related('user','project').filter(Q(project__id=project_id) & Q(user__id=user_dict['id']))
            except (Project.DoesNotExist, ValueError):
                return Response({'Error': "Please Enter Valid Project ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            assets=Asset.objects.select_related('user').filter(user__id=user_dict['id'])
        assets_data=AssetSerializer(assets,many=True).data
        return Response({'data': assets_data},
                        status=status.HTTP_200_OK)
    
    @auth_user
    def post(self,request,user_dict):
        file=request.data.get('asset',None)
        project=request.data.get('project',None)
        force=request.query_params.get('force','false')
        if not file or not file.name:
            return Response({'Error':"No Asset Provided"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if file.size*(1e-6) > 5:
            return Response({'Error':"File size cannot be greater than 5MB"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if project:
            try:
                project = Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id != user_dict['id']:
                    return Response({'Error': "The project does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Project.DoesNotExist, ValueError):
                return Response({'Error': "Please Enter Valid Project ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        file.name=get_valid_filename(file.name)
        files_with_same_name=Asset.objects.select_related('user').filter(Q(filename__exact=file.name) & Q(user__id=user_dict['id']))
        files_with_same_name_count=files_with_same_name.count()
        if files_with_same_name_count>0:
            if not force=='true':
                return Response({'Error':"Files with same name already exists"},
                                status=status.HTTP_409_CONFLICT)
                
        object_key=f'user_{user_dict["id"]}/{file.name}:{datetime.now().isoformat()}'
        res=upload_to_s3(file,object_key)
        if res==False:
            return Response({'Error':"Failed to Upload Asset"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        asset_url=f'{settings.S3_LOCATION}{object_key}'
        if files_with_same_name_count>0:
            asset=files_with_same_name[0]
            deleted=delete_from_s3(asset.url)
            if not deleted:
                return Response({"Error":"Failed to Upload Asset"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            custom_payload={
                'url':asset_url,
                'updated_at':date.today().isoformat(),
                'filename':file.name,
                'project':project
            }
            asset_serializer=AssetSerializer(asset,data=custom_payload,partial=True)
        else:
            custom_payload={
            'user':user_dict['id'],
            'url':asset_url,
            'created_at':date.today().isoformat(),
            'updated_at':date.today().isoformat(),
            'filename':file.name,
            'project':project
            }
            asset_serializer=AssetSerializer(data=custom_payload)
    
        if asset_serializer.is_valid():
            asset_serializer.save()
            asset_json=asset_serializer.data
            return Response({'data': asset_json},
                            status=status.HTTP_200_OK)
        
        else:
            return Response(asset_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_asset
    def put(self,request,user_dict,asset):
        payload=request.data
        if 'url' in payload:
            del payload['url']
        project=payload.get('project',None)
        filename=payload.get('filename',None)
        if project:
            try:
                project = Project.objects.select_related('contact').get(id=project)
                if project.contact.user.id != user_dict['id']:
                    return Response({'Error': "The project does not belong to the user"},
                                    status=status.HTTP_403_FORBIDDEN)
            except (Project.DoesNotExist, ValueError):
                return Response({'Error': "Please Enter Valid Project ID"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        if filename:
            files_with_same_name=Asset.objects.select_related('user').filter(Q(filename__exact=filename) & Q(user__id=user_dict['id'])).count()
            if files_with_same_name>0:
                return Response({'Error':"Files with same name already exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        payload['updated_at']=date.today().isoformat()
        asset_serializer=AssetSerializer(asset,data=payload,partial=True)
    
        if asset_serializer.is_valid():
            asset_serializer.save()
            asset_json=asset_serializer.data
            return Response({'data': asset_json},
                            status=status.HTTP_200_OK)
        
        else:
            return Response(asset_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    @auth_user
    @auth_asset
    def delete(self,request,user_dict,asset):
        url=asset.url
        deleted=delete_from_s3(url)
        if deleted:
            asset.delete()
            return Response({'Message':"Asset Deleted Successfully"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"Error":"Failed to delete Asset"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        