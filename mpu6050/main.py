# Example code for (GY-521) MPU6050 Accelerometer/Gyro Module
# Write in MicroPython by Warayut Poomiwatracanont JAN 2023

from MPU6050 import MPU6050

from os import listdir, chdir
from machine import Pin
from time import sleep_ms
import time


mpu = MPU6050(scl=21, sda=22)

def calibrate_gyro_z(samples=100, delay=0.01):
    print("请保持静止，正在校准陀螺仪...")
    sum_z = 0
    for _ in range(samples):
        gyro = mpu.read_gyro_data()
        sum_z += gyro['z']
        time.sleep(delay)
    bias = sum_z / samples
    print("校准完成，偏移值：{:.4f}°/s".format(bias))
    return bias

last_time = time.ticks_ms()

def get_dt():
    global last_time
    now = time.ticks_ms()
    dt = time.ticks_diff(now, last_time) / 1000
    last_time = now
    return dt


def main():
    gyro_z_bias = calibrate_gyro_z(samples=500)
    print('biasZ:', gyro_z_bias)
    yaw = 0.0

    while True:
        # Accelerometer Data
        # accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
        # aX = accel["x"]
        # aY = accel["y"]
        # aZ = accel["z"]
        # print(f"accel x:{aX} y:{aY} z:{aZ}")
    
        # Gyroscope Data
        dt = get_dt()
        gyro = mpu.read_gyro_data()   # read the gyro [deg/s]
        gX = gyro["x"]
        gY = gyro["y"]
        gZ = gyro["z"]
        corrected_z = gZ - gyro_z_bias
        yaw += corrected_z * dt
        yaw %= 360
        print("Yaw: {:.2f}°".format(yaw))
        time.sleep(0.02)

        # print(f"gyro x:{gX} y:{gY} z:{gZ} deg/s")
        # print(f"gyro z:{gZ - gyro_z_bias}")
    
        # Rough Temperature
        temp = mpu.read_temperature()   # read the device temperature [degC]
        # print(f"Temperature: {temp}°C")

        # G-Force
        # gforce = mpu.read_accel_abs(g=True) # read the absolute acceleration magnitude
        # print("G-Force: " + str(gforce))
        
        # Time Interval Delay in millisecond (ms)
        sleep_ms(100)

if __name__ == '__main__':
    main()