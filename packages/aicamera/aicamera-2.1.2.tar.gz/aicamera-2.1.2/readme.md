## author  周靖松  15032985110


``` python


import aicamera

# 初始化  必须第一步 默认启动人脸检测模型
aicamera.init()

# 获取屏幕宽高
aicamera.lcd.get_height()
aicamera.lcd.get_width()


# wifi 是否连接
aicamera.wifi.is_connected()

# 打印模型类型
print(aicamera.modeType.keys())
# dict_keys(['face_detect', 'traffic_sign', 'qr_code', 'bar_code', 'face_recognition', 'classify', 'gesture', 'car_number', 'trace'])


# 切换模型
aicamera.use_mode('face_detect')

# 获取当前模型返回值(需要先切换模型才能获取返回值)
aicamera.get_res()

# 获取当前模型标签(标签目前不能中文 有异议@白睿 需要先切换模型才能获取返回值)
aicamera.get_tags()

# 获取当前帧并保存
img = aicamera.image.take_photo()
aicamera.image.save(img)

```
