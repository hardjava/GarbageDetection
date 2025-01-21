import serial
import time

# 시리얼 포트 설정
ser = serial.Serial('COM3', 9600)
time.sleep(2)  # 포트 준비 시간 대기

# 데이터 전송x   (문자열을 바이트로 변환)
ser.write(b'0')  # '1'을 바이트 형식으로 변환
print("데이터 전송 완료!")

while True:
    if ser.in_waiting > 0:  # 수신된 데이터가 있는지 확인
        data = ser.readline().decode('utf-8').rstrip()  # 바이트 데이터를 문자열로 디코딩
        print("수신 데이터:", data)
        break

ser.close()  # 포트 닫기
