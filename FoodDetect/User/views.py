from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from FoodDetect.settings import MEDIA_ROOT
from Ingredient.models import Ingredient
from Ingredient.serializers import IngredientSerializer
from rest_framework.response import Response
from .models import History, Favorites
import os
from rest_framework import serializers
from Ingredient.models import Ingredient


class IngredientOcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('ingredient_id', 'chinese_name', 'english_name', 'introduction', 'effects', 'rating', 'potential_risk_people',
        'daily_intake_recommendation')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        res = {
            "scores": data['rating'],
            "arr": data['chinese_name'],
        }
        return {
            'id':data['ingredient_id'],
            'res':res
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
        results = ['磷酸氢二钾', '大豆分离蛋白','wbg牛逼']
        final_list = []
        for item in results:
            ingredient = Ingredient.objects.filter(chinese_name=item).first()
            if ingredient:
                serializer = IngredientOcrSerializer(instance=ingredient)
                data = serializer.data
                data['imgUrl'] = 'http://127.0.0.1:8000'+target_path
                final_list.append(data)
            else:
                final_list.append({
                    '配料名':item,
                    'error':'抱歉，数据库中没有找到这个配料信息'})

        '''
        存储历史记录，同时数据库事件回滚等
        '''


        return Response(final_list)

class FavorView(APIView):
    def