import time
import usb_hid
import board
import digitalio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# 配置音量控制、鼠标控制和键盘控制
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

# 初始化计时器和状态
last_activity_time = time.time()
move_right = True  # 用于控制鼠标移动方向

# 定义一个GPIO做检测的终端输入，内部上拉
button_pin = digitalio.DigitalInOut(board.GP10)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP

def take_photo():
    # 尝试使用不同的按键进行拍照
    # 方法1: 使用播放/暂停键
    cc.send(ConsumerControlCode.PLAY_PAUSE)
    # 方法2: 使用键盘相机键
    # keyboard.send(Keycode.CAMERA)
    # 方法3: 使用组合键
    # keyboard.press(Keycode.CONTROL, Keycode.P)
    # keyboard.release_all()

def prevent_sleep():
    global last_activity_time, move_right
    if time.time() - last_activity_time >= 15:
        if move_right:
            mouse.move(x=10, y=0)  # 向右移动10个单位
        else:
            mouse.move(x=-10, y=0)  # 向左移动10个单位
        move_right = not move_right  # 改变移动方向
        last_activity_time = time.time()

def check_button():
    if not button_pin.value:
        time.sleep(0.05)  # 简单的去抖动
        if not button_pin.value:
            take_photo()
            while not button_pin.value:  # 持续检测，直到按钮释放
                time.sleep(0.01)

while True:
    time.sleep(0.1)  # 每秒执行10次
    prevent_sleep()
    check_button()