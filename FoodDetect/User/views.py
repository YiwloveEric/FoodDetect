from rest_framework import status
from rest_framework.views import APIView


from rest_framework.response import Response
from .models import  Users
import os
from rest_framework import serializers
from Ingredient.models import Ingredient
import requests
from FoodDetect.settings import APPID, SECRET,MEDIA_ROOT
import json


class IngredientOcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'ingredient_id', 'chinese_name', 'english_name', 'introduction', 'effects', 'rating',
            'potential_risk_people',
            'daily_intake_recommendation')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        res = {
            "scores": data['rating'],
            "arr": data['chinese_name'],
        }
        return {
            'id': data['ingredient_id'],
            'res': res
        }


# Create your views here.

class OCRIngredient(APIView):
    def post(self, request):
        # 获取图片
        pic = request.data.get('file1')
        type = pic.content_type
        if type not in ['image/jpg', 'image/png', 'image/jpeg']:
            return Response({'error': '您上传的照片不支持，只能支持jpg和png格式的照片'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 构建目标文件夹路径
        target_folder = MEDIA_ROOT
        # 确保目标文件夹存在
        os.makedirs(target_folder, exist_ok=True)

        # 构建目标文件路径
        target_path = os.path.join(target_folder, pic.name)

        # 保存文件
        with open(target_path, 'wb') as f:
            f.write(pic.read())
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
                data['imgUrl'] = 'http://127.0.0.1:8000' + target_path
                final_list.append(data)
            else:
                final_list.append({
                    '配料名': item,
                    'error': '抱歉，数据库中没有找到这个配料信息'})

        '''
        存储历史记录，同时数据库事件回滚等
        '''

        return Response(final_list)


class LoginView(APIView):
    def post(self, request):
        username = request.query_params.get('username')
        used = Users.objects.filter(name=username).first()
        if used:
            return Response({'error': '名字已存在，请更改你的名字'}, status=status.HTTP_400_BAD_REQUEST)
        js_code = request.query_params.get('js_code')
        appid = APPID
        secret = SECRET
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}&grant_type=authorization_code"
        res = requests.get(url).text
        response_data = json.loads(res)

        session_key = response_data["session_key"]
        openid = response_data["openid"]
        user = Users(name=username, openid=openid)
        user.save()
        return Response({'session_key': session_key})


class FavorView(APIView):
    pass
