import time
import usb_hid
import board
import digitalio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

# 配置音量控制和鼠标控制
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# 初始化计时器和状态
last_activity_time = time.time()

# 定义一个GPIO做检测的终端输入，内部上拉
button_pin = digitalio.DigitalInOut(board.GP10)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP

def take_photo():
    cc.send(ConsumerControlCode.VOLUME_DECREMENT)

while True:
    time.sleep(0.1)  # 每秒执行一次

    # 检查是否已经过了15秒
    if time.time() - last_activity_time >= 15:
        # 模拟一次鼠标移动以防止休眠
        mouse.move(x=10, y=0)  # 向右移动10个单位
        # 重置计时器
        last_activity_time = time.time()

    # 检查GPIO引脚是否被拉低
    if not button_pin.value:
        # 立即触发一次相机拍照
        take_photo()
        # 等待按钮释放（去抖动）
        while not button_pin.value:
            time.sleep(0.01)
