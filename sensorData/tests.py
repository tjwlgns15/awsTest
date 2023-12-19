import base64
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import timedelta
from django.utils import timezone
from django.views.generic import ListView, TemplateView
from .models import Data
from .forms import DateRangeForm


class Test1(ListView):
    model = Data
    template_name = 'sensorData/test.html'
    context_object_name = 'sensor_data_list'  # 템플릿에서 사용할 컨텍스트 변수 이름
    ordering = ['-time_stamp']
    paginate_by = 10

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
            # print(time_list[-1])
            # print(time_list[0])

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



class Test2(ListView):
    model = Data
    template_name = 'sensorData/test2.html'
    context_object_name = 'sensor_data_list'  # 템플릿에서 사용할 컨텍스트 변수 이름
    ordering = ['-time_stamp']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET)

        # sensor_data_list = Data.objects.all().order_by('-time_stamp')
        sensor_data_list = Data.objects.all().order_by('-time_stamp')[:2500]

        # print(sensor_data_list[0].light)

        # 개수가 모자를 경우 Error
        for data in sensor_data_list:
            data.time_stamp = data.time_stamp - timedelta(hours=9)

        context['sensor_data_list'] = sensor_data_list
        # print(context['sensor_data_list'][0].time_stamp)

        sensor_data_list = Data.objects.all().order_by('-time_stamp')[:2500]
        # print(sensor_data_list[0].time_stamp)


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
        # print('light_list', light_list)

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

            end_date = end_date + timedelta(days=1) - timedelta(hours=9)  # 오늘 날짜까지 포함하도록 변경
            # print(start_date)
            # print(end_date)

            # 데이터베이스에서 선택된 기간 내의 데이터를 조회
            sensor_data_list = Data.objects.filter(time_stamp__range=[start_date, end_date]).order_by('-time_stamp')
            # print(sensor_data_list)

            a = Data.objects.filter(time_stamp__range=[start_date, end_date]).order_by('-time_stamp').values_list(
                'time_stamp', flat=True)
            a_list = list(a)
            if a_list:
                print(a_list[0])  # 첫 번째 항목
                print(a_list[-1])  # 마지막 항목
            else:
                print("No data found")

            context['sensor_data_list'] = sensor_data_list
            # print(context['sensor_data_list'][0].time_stamp)


            # datetime객체는 json으로 직렬화 할 수 없음 -> 형식을 변환
            time_list = [data.time_stamp for data in sensor_data_list]
            # print(time_list[-1])
            # print(time_list[0])

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

            # print(context['sensor_data_list'])
            # print(context['json_data'])

        context['form'] = form

        # 오브젝트 확인
        # ob1 = context['sensor_data_list']
        # for data in ob1:
            # print(data.time_stamp)
            # print(data.sensor_data['O2_1'])
        # print(json_data['time_list'])

        return context



    @csrf_exempt
    def save_image(request):
        if request.method == 'POST':
            image_data = request.POST.get('imageData', None)
            if image_data:
                # 이미지를 저장할 위치를 결정합니다
                save_location = "sensorData/static/images/my_saved_image.png"  # 실제 경로로 수정해야 합니다

                # Base64로 인코딩된 이미지 데이터를 올바르게 디코드하고 저장합니다
                try:
                    image_data = base64.b64decode(image_data)
                    with open(save_location, 'wb') as f:
                        f.write(image_data)

                    # 저장된 위치를 콘솔에 출력합니다
                    print("이미지가 다음 위치에 저장되었습니다:", save_location)

                    return HttpResponse('이미지가 성공적으로 저장되었습니다.')
                except Exception as e:
                    print("이미지 저장 중 오류 발생:", str(e))

        return HttpResponse('이미지가 저장되지 않았습니다.')