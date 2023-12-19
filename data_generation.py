import os
import sys
import time
import random
import numpy as np
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta
import pytz



# Django 프로젝트의 경로를 Python 경로에 추가합니다.
sys.path.append('C:/Users/SOLMI/PycharmProjects/pythonProject')  # Django 프로젝트 디렉토리 경로
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# Django를 초기화합니다.
import django
django.setup()




from sensorData.models import Data

def generate_and_save_sensor_data():
    while True:

        # 서울 시간대로 현재 시간을 얻기
        seoul_timezone = pytz.timezone('Asia/Seoul')
        time_stamp = datetime.now(seoul_timezone)
        # time_stamp = timezone.now()
        print(time_stamp)


        # 각 데이터 필드에 대한 최대 및 최소 값 설정
        field_ranges = {
            "DO": {"min_value": 4.0, "max_value": 8.0},
            "pH": {"min_value": 6.0, "max_value": 8.0},
            "O2_1": {"min_value": 20.0, "max_value": 30.0},
            "flow": {"min_value": 0.0, "max_value": 10.0},
            "CO2_1": {"min_value": 30.0, "max_value": 60.0},
            "photo": {"min_value": 0.0, "max_value": 80.0},
            "humidity": {"min_value": 40.0, "max_value": 60.0},
            "temperature1": {"min_value": 20.0, "max_value": 30.0},
        }

        # 각 데이터 필드에 대해 주기성 값 할당
        random_data = {}
        for field, value_range in field_ranges.items():
            min_value = value_range["min_value"]
            max_value = value_range["max_value"]
            # 무작위 값 생성
            random_value = random.uniform(min_value, max_value)
            noise = random.uniform(-0.1, 0.1)
            random_data[field] = round(random_value + noise, 2)


        # Data 객체를 생성하고 데이터베이스에 저장합니다
        data_entry = Data(sensor_data=random_data, time_stamp=time_stamp)
        data_entry.save()

        # 10초 동안 대기합니다
        time.sleep(10)

if __name__ == "__main__":
    generate_and_save_sensor_data()
