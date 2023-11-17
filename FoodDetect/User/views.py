from rest_framework import status
from rest_framework.views import APIView

from rest_framework.response import Response
from User.models import Users, History, Favorites
import os
from Ingredient.models import Ingredient
import requests
from FoodDetect.settings import APPID, SECRET, MEDIA_ROOT
import json
import uuid
from Ingredient.serializers import IngredientSerializer, IngredientOcrSerializer
from User.serializers import ReviewFavorViewSerializer, UsersSerializer
import hashlib
from django_redis import get_redis_connection
import base64


# Create your views here.

class OCRIngredient(APIView):
    '''
    这个view类是用户上传图片，然后通过ocr算法，返回图片内容
    '''

    def post(self, request):
        '''
        username
        imgBase64
        :param request:
        :return:
        '''
        # 获取用户信息
        # username = request.data.get('username')
        # user = Users.objects.filter(name=username).first()
        # if user is None:
        # return Response({'error': '您未注册，请先注册'},
        # status=status.HTTP_400_BAD_REQUEST)
        # 获取图片
        pic = request.data.get('imgBase64')
        # type = pic.content_type
        pic = base64.b64decode(pic)
        # if type not in ['image/jpg', 'image/png', 'image/jpeg']:
        #     return Response({'error': '您上传的照片不支持，只支持jpg、png、jpeg格式的照片'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        # file_extension = pic.name.split('.')[-1]
        file_extension = "jpg"
        unique_filename = str(uuid.uuid4()) + '.' + file_extension
        # 构建目标文件夹路径
        target_folder = MEDIA_ROOT
        # 确保目标文件夹存在
        os.makedirs(target_folder, exist_ok=True)

        # 构建目标文件路径
        target_path = os.path.join(target_folder, unique_filename)

        # 保存文件
        with open(target_path, 'wb') as f:
            f.write(pic)
        '''
        经过校验后存储图片，并将图片发送给ocr算法
        '''
        # 假设ocr输出结果是[磷酸氢二钾,大豆分离蛋白]
        results = ['磷酸氢二钾', '大豆分离蛋白', 'wbg牛逼']
        final_list = []
        for item in results:
            ingredient = Ingredient.objects.filter(chinese_name=item).first()
            if ingredient:
                serializer = IngredientOcrSerializer(instance=ingredient)
                data = serializer.data
                imageUrl = 'http://127.0.0.1:8000' + target_path
                data['imgUrl'] = imageUrl
                final_list.append(data)
            else:
                final_list.append({
                    '配料名': item,
                    'error': '抱歉，数据库中没有找到这个配料信息'})

        '''
        存储历史记录，同时数据库事件回滚等
        '''
        # his = History(user_id=user.user_id, image=imageUrl)
        # his.save()
        return Response(final_list)


class ProLoginView(APIView):
    import jwt
    import datetime
    from jwt import exceptions
    def post(self,request):
        user = request.data.get('')

class LoginView(APIView):
    '''
    这个view类是进行用户的注册登录
    '''

    # authentication_classes = []

    def post(self, request):
        '''
        这个视图类需要用户姓名，以及前端传过来的js_code
        username
        js_code
        :param request:
        :return:
        '''
        username = request.data.get('username')
        used = Users.objects.filter(name=username).first()
        # 校验姓名
        # if used:
        #     return Response({'error': '名字已存在，请更改你的名字'}, status=status.HTTP_400_BAD_REQUEST)
        js_code = request.data.get('js_code')
        appid = APPID
        secret = SECRET
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}&grant_type=authorization_code"
        res = requests.get(url).content
        # 与微信API连接，获取openid与sessionKey
        response_data = json.loads(res)
        # 判断是否有错误码
        if 'errcode' in response_data:
            return Response(data={'code': response_data['errcode'], 'msg': response_data['errmsg']})
        # 登录成功
        openid = response_data['openid']
        session_key = response_data['session_key']
        # 保存openid,需要先判断数据库中有没有这个openid
        user, created = Users.objects.get_or_create()

        user_str = str(UsersSerializer(user).data)
        # 生成自定义登录态，返回给前端
        sha = hashlib.sha1()
        sha.update(openid.encode())
        sha.update(session_key.encode())
        digest = sha.hexdigest()
        # 将自定义登录态保存到缓存中, 两个小时过期
        conn = get_redis_connection('default')
        conn.set(digest, user_str, ex=2 * 60 * 60)
        return Response(data={'code': 200, 'msg': 'ok', 'data': {'skey': digest}})


class RegisFavorView(APIView):
    '''
    这个view类是进行注册收藏夹
    '''

    def post(self, request):
        '''
        这个视图类需要用户名称，历史记录id，note记录
        username
        history_id
        note
        :param request:
        :return:
        '''
        username = request.data.get('username')
        history_id = request.data.get('history_id')
        note = request.data.get('note')
        # 获取用户信息
        user = Users.objects.filter(name=username).first()
        if user:
            his = History.objects.filter(history_id=history_id).filter(user_id=user.user_id).first()
            if his:
                fav = Favorites(user_id=user.user_id, history_id_id=his.history_id, note=note)
                fav.save()
                return Response(data=request.data)
            else:
                return Response({'error': '历史记录不存在，请重新拍照片上传生成记录'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '您未注册，请先注册'},
                            status=status.HTTP_400_BAD_REQUEST)


class ReviewFavorView(APIView):
    '''
    这个视图类进行返回用户收藏夹记录:还有bug
    '''

    def get(self, request):
        '''
        username
        favorites_id
        :param request:
        :return:
        '''
        # 获取用户姓名
        username = request.query_params.get('username')
        # 获取收藏夹id
        favorites_id = request.query_params.get('favorites_id')
        user = Users.objects.filter(name=username).first()
        if user:
            # 获取数据
            fav = Favorites.objects.filter(favorites_id=favorites_id).filter(user_id=user.user_id).first()
            if fav:
                # 获取history_id查找历史记录
                history_id = fav.history_id.history_id
                # 获取土拍你url地址
                history = History.objects.filter(history_id=history_id).first()
                img_url = history.image.path
                '''
                将图片重新传给OCR算法
                '''
                # 假设算法输出的结果为下
                results = ['磷酸氢二钾', '大豆分离蛋白', 'wbg牛逼']
                final_list = []
                for item in results:
                    ingredient = Ingredient.objects.filter(chinese_name=item).first()
                    if ingredient:
                        serializer = IngredientOcrSerializer(instance=ingredient)
                        data = serializer.data
                        data['imgUrl'] = img_url
                        final_list.append(data)
                    else:
                        final_list.append({
                            '配料名': item,
                            'error': '抱歉，数据库中没有找到这个配料信息'})
                return Response(final_list)
            else:
                return Response({'error': '没有这项收藏记录，请先进行收藏'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': '您未注册，请先注册'},
                            status=status.HTTP_400_BAD_REQUEST)
