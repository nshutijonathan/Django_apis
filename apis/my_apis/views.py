from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import MyFriendList


class MyFriend(View):
    def get(self, request):
        friend_list = list(MyFriendList.objects.values())
        if len(friend_list) == 0:
            return JsonResponse({"error": "the list is empty"})
        return JsonResponse(friend_list, safe=False)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MyFriend, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        data = request.body.decode('utf8')
        data = json.loads(data)
        try:
            new_friend = MyFriendList(friend_name=data["friend_name"], mobile_no=data["mobile_no"])
            new_friend.save()
            return JsonResponse({"created": data}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)


class MyFriendDetail(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MyFriendDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        friend_list = {"friend": list(
            MyFriendList.objects.filter(pk=pk).values())}
        return JsonResponse(friend_list, safe=False)

    def put(self, request, pk):
        data = request.body.decode('utf8')
        data = json.loads(data)
        try:
            new_friend = MyFriendList.objects.get(pk=pk)
            data_key = list(data.keys())
            for key in data_key:
                if key == "friend_name":
                    new_friend.friend_name = data[key]
                if key == "mobile_no":
                    new_friend.mobile_no = data[key]
            new_friend.save()
            return JsonResponse({"updated": data}, safe=False)
        except MyFriendList.DoesNotExist:
            return JsonResponse({"error": "Your friend having provided key does not exist"}, safe=False)
        except:
            return JsonResponse({"error": "not a valid data"}, safe=False)

    def delete(self, request, pk):
        try:
            new_friend = MyFriendList.objects.get(pk=pk)
            new_friend.delete()
            return JsonResponse({"deleted": True}, safe=False)
        except:
            return JsonResponse({"error": "not a valid primary key"}, safe=False)
