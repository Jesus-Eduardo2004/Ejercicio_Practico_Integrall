import machine
import ssd1306
import time

pot = machine.ADC(machine.Pin(32))
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

buzzer = machine.Pin(15, machine.Pin.OUT)
buzzer_pwm = machine.PWM(buzzer)

rojo = machine.Pin(17, machine.Pin.OUT)
verde = machine.Pin(18, machine.Pin.OUT)
azul = machine.Pin(19, machine.Pin.OUT)

def activar_buzzer():
    buzzer_pwm.freq(1000)
    buzzer_pwm.duty(512)
    time.sleep(0.5)
    buzzer_pwm.duty(0)

def set_led_color(r, g, b):
    rojo.value(r)
    verde.value(g)
    azul.value(b)

def draw_tank(x, y, width, height, fill_percentage):
    oled.rect(x, y, width, height, 1)
    fill_height = int((fill_percentage / 100) * height)
    oled.fill_rect(x + 1, y + height - fill_height, width - 2, fill_height, 1)

def mostrar_tanque():
    while True:
        valor = pot.read()
        porcentaje = int((valor / 4095) * 100)

        oled.fill(0)
        draw_tank(50, 10, 28, 44, porcentaje)
        oled.text(str(porcentaje) + '%', 50, 55, 1)

        if porcentaje < 30:
            set_led_color(0, 1, 0)  
        elif 30 <= porcentaje < 60:
            set_led_color(0, 0, 1) 
        else:
            activar_buzzer()
            set_led_color(1, 0, 0)  

        oled.show()
        time.sleep(0.1)


mostrar_tanque()
