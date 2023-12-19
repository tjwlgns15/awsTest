import json
from datetime import timedelta
from datetime import datetime

from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from .models import Data

from django.shortcuts import render
from .models import Data
from .forms import DateRangeForm


class SensorDataHome(TemplateView):
    template_name = 'sensorData/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 데이터베이스에서 데이터 가져오기
        data_list = Data.objects.order_by('-time_stamp')[1:6]  # 최신 1개 뺀 5개
        # print("data_list : ", data_list)
        # for data_obj in data_list:
        #     print(data_obj.light)

        # "Timestamp" 필드의 형식을 변경
        data_time = [data.time_stamp for data in data_list]
        # formatted_timestamps = [timestamp.strftime("%Y. %m. %d, %I:%M:%S %p") for timestamp in data_time]

        temp = [data.temp for data in data_list]
        sound = [data.sound for data in data_list]
        light = [data.light for data in data_list]
        # print(sensor_data)
        sensor_data_and_timestamps = list(zip(temp, sound, light, data_time))
        # print('sensor_data_and_timestamps :', sensor_data_and_timestamps)

        recent_sensor_data = Data.objects.order_by('-time_stamp').first()  # 최신 1개
        # print("recent_sensor_data", recent_sensor_data)


        # print(sensor_data)
        # print(formatted_timestamps)
        # print(sensor_data_and_timestamps)
        # for i in sensor_data_and_timestamps:
        #     print(i)

        # O2_list = []
        # CO2_list = []
        #
        # for data_obj1 in sensor_data:
        #     O2_list.append(data_obj1.get("O2_1", None))
        #     print(O2_list)
        #
        # for data_obj2 in sensor_data:
        #     CO2_list.append(data_obj2.get("CO2_1", None))
        #     print(CO2_list)


        # print(ph_list)



        context = {
            # 'O2_list': O2_list,
            # 'CO2_list': CO2_list,
            'sensor_data_and_timestamps': sensor_data_and_timestamps,
            'recent_sensor_data': recent_sensor_data,
        }
        # print(context)

        return context  # JSON 응답 생성 대신 컨텍스트 반환


class SensorDataListView(ListView):
    model = Data
    template_name = 'sensorData/data_list.html'
    context_object_name = 'sensor_data_list'  # 템플릿에서 사용할 컨텍스트 변수 이름
    ordering = ['-time_stamp']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET)

        # sensor_data_list = Data.objects.all().order_by('-time_stamp')
        sensor_data_list = Data.objects.all().order_by('-time_stamp')[:2500]
        # print(sensor_data_list[0].time_stamp)
        # print(sensor_data_list[len(sensor_data_list)-1].time_stamp)

        for data in sensor_data_list:
            data.time_stamp -= timedelta(hours=9)



        context['sensor_data_list'] = sensor_data_list
        # print(context['sensor_data_list'][0].time_stamp)

        sensor_data_list = Data.objects.all().order_by('-time_stamp')[:2500]
        # print(sensor_data_list[0].time_stamp)
        # print(sensor_data_list[len(sensor_data_list) - 1].time_stamp)



        # datetime객체는 json으로 직렬화 할 수 없음 -> 형식을 변환
        time_list = [data.time_stamp for data in sensor_data_list]

        # print(time_list[0])
        # time_list = [data.strftime('%Y-%m-%dT%H:%M:%S%z') for data in time_list]
        # print(time_list[-1])
        # print(time_list[0])
        # print(type(time_list))


        temp_list = [data.temp for data in sensor_data_list]
        sound_list = [data.sound for data in sensor_data_list]
        light_list = [data.light for data in sensor_data_list]

        # print('time_list', time_list)
        # print('temp_list', temp_list)
        # print('sound_list', sound_list)

        # JSON 데이터
        json_data = {
            'time_list': time_list,
            'temp_list': temp_list,
            'sound_list': sound_list,
            'light_list': light_list,
        }


        # json_data의 'time_list'를 문자열로 변환
        for i in range(len(json_data['time_list'])):
            json_data['time_list'][i] = json_data['time_list'][i].isoformat()

        # JSON으로 변환
        context['json_data'] = json.dumps(json_data)

        # print(context.keys())
        # print(context['sensor_data_list'][0].time_stamp)

        # parsed_data = json.loads(context['json_data'])
        # time_list = parsed_data.get("time_list")
        # print(time_list)


        # print(context['sensor_data_list'])
        # print(context['json_data'])
        # print(type(context['json_data']))

        # 기간 조회 폼
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            end_date = end_date + timedelta(days=1)

            # 데이터베이스 시간대에서 Django 시간대로 변환
            start_date = timezone.make_aware(start_date, timezone.utc)
            end_date = timezone.make_aware(end_date, timezone.utc)

            # 데이터베이스에서 선택된 기간 내의 데이터를 조회
            sensor_data_list = Data.objects.filter(time_stamp__range=[start_date, end_date]).order_by('-time_stamp')
            # print(len(sensor_data_list))
            # print(sensor_data_list[0].time_stamp)
            # print(sensor_data_list[len(sensor_data_list) - 1].time_stamp)


            # 시간이 왜 자꾸 9시간 ++ 되는지 모르겠음
            for data in sensor_data_list:
                data.time_stamp -= timedelta(hours=9)
            # print(sensor_data_list[0].time_stamp)
            # print(sensor_data_list[len(sensor_data_list) - 1].time_stamp)

            # print(sensor_data_list)
            # a = Data.objects.filter(time_stamp__range=[start_date, end_date]).order_by('-time_stamp').values_list(
            #     'time_stamp', flat=True)
            # a_list = list(a)
            # if a_list:
            #     print(a_list[0])  # 첫 번째 항목
            #     print(a_list[-1])  # 마지막 항목
            # else:
            #     print("No data found")

            context['sensor_data_list'] = sensor_data_list
            # print(context['sensor_data_list'][0].time_stamp)

            # 차트, 테이블의 시간이 안 맞아서 다시 호출(그래프에 사용)
            sensor_data_list = Data.objects.filter(time_stamp__range=[start_date, end_date]).order_by('-time_stamp')

            # datetime객체는 json으로 직렬화 할 수 없음 -> 형식을 변환
            time_list = [data.time_stamp for data in sensor_data_list]
            # print(time_list[0])
            # print(time_list[-1])

            temp_list = [data.temp for data in sensor_data_list]
            sound_list = [data.sound for data in sensor_data_list]
            light_list = [data.light for data in sensor_data_list]
            # print(temp_list)


            # JSON 데이터
            json_data = {
                'time_list': time_list,
                'temp_list': temp_list,
                'sound_list': sound_list,
                'light_list': light_list,
            }


            # json_data의 'time_list'를 문자열로 변환
            for i in range(len(json_data['time_list'])):
                json_data['time_list'][i] = json_data['time_list'][i].isoformat()

            # JSON으로 변환
            context['json_data'] = json.dumps(json_data)
            # JSON 데이터를 문자열로 변환하여 컨텍스트에 추가
            # print(context)

            # print(context['sensor_data_list'].count())
            # print(context['json_data'])

        context['form'] = form

        # 오브젝트 확인
        # ob1 = context['sensor_data_list']
        # for data in ob1:
            # print(data.time_stamp)
            # print(data.sensor_data['O2_1'])
        # print(json_data['time_list'])

        return context





class Update(View):
    def get(self, request, *args, **kwargs):
        # JSON으로 반환하려는 데이터 검색
        data_list = Data.objects.order_by('-time_stamp')[1:21]
        # print("data_list : ", data_list.count())
        recent_data = Data.objects.order_by('-time_stamp')[0]

        time_list = [data.time_stamp for data in data_list]
        temp_list = [data.temp for data in data_list]
        sound_list = [data.sound for data in data_list]
        light_list = [data.light for data in data_list]

        # 최신 데이터에서 관련 필드 추출
        data_list_dict = {
            'temp_list': temp_list,
            'sound_list': sound_list,
            'time_list': time_list,
            'light_list': light_list,
        }
        recent_data_dict = {
            "temp": recent_data.temp,
            "sound": recent_data.sound,
            "light": recent_data.light,
            # 필요한 경우 더 많은 필드 추가
        }



        data_dict = {
            'data_list': data_list_dict,
            'recent_data': recent_data_dict,
        }

        # 데이터를 JSON 응답으로 반환
        return JsonResponse(data_dict)




# Arduino
import requests
from django.http import JsonResponse

def toggle_light(request, command):
    # ESP32의 IP 주소 및 포트 번호
    esp32_url = 'http://1.245.119.116:28080/'

    # 요청을 보낼 명령
    if command == 'H' or command == 'L':
        # ESP32로 GET 요청을 보내어 조명을 토글 (예를 들어, 'H'와 'L'을 사용)
        response = requests.get(esp32_url + command)

        # ESP32로부터 받은 응답에 따라 처리할 내용
        if response.status_code == 200:
            # 요청이 성공했을 때 수행할 작업
            return JsonResponse({'message': 'Light toggled successfully.'})
        else:
            # 요청이 실패했을 때 수행할 작업
            return JsonResponse({'error': 'Failed to toggle light.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid command.'}, status=400)

