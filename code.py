from m5stack import *
from m5stack_ui import *
from uiflow import *
from easyIO import *
from m5stack import mic
from m5stack import lcd
import wifiCfg

# [Description]
# Contains individual questions from the survey
#
# [Parameters]
# question[str] : The question to ask the user
# A[str]: Option corresponding to button A (left)
# B[str]: Option corresponding to button B (middle)
# C[str]: Option corresponding to button C (right)
#
# [Methods]
# Getter methods
# display(): displays the question and options to the user; awaits response

class Question:
  def __init__(self, question, A="Yes", B="Maybe", C="No"):
    self.__question = question
    self.__A = A
    self.__B = B
    self.__C = C

  def getQuestion(self):
    return self.__question

  def getA(self):
    return self.__A

  def getB(self):
    return self.__B

  def getC(self):
    return self.__C

  def display(self):
    screen.clean_screen()
    font = FONT_MONT_22

    if len(self.__question) > 20:
      font = FONT_MONT_18

    question_label = M5Label(self.__question, color=0x000, font=font, parent=None)
    question_label.set_align(ALIGN_CENTER, x=0, y=-80, ref=screen.obj)

    A_label = M5Label(self.__A, color=0x000, font=FONT_MONT_18, parent=None)
    A_label.set_align(ALIGN_IN_BOTTOM_LEFT, x=40, y=-10, ref=screen.obj)

    B_label = M5Label(self.__B, color=0x000, font=FONT_MONT_18, parent=None)
    B_label.set_align(ALIGN_CENTER, x=0, y=100, ref=screen.obj)

    C_label = M5Label(self.__C, color=0x000, font=FONT_MONT_18, parent=None)
    C_label.set_align(ALIGN_IN_BOTTOM_RIGHT, x=-40, y=-10, ref=screen.obj)


    while True:
      if btnA.wasPressed():
        break;
      elif btnB.wasPressed():
        break;
      elif btnC.wasPressed():
        break;

# [Description]
# Makes the device vibrate for a specific amount of time
#
# [Parameters]
# intensity[int] : the strength of the vibration
# time_ms[int]: the duration of the vibration in ms
#
# [Return]
# None

def vibrate(intensity : int, time_ms : int):
  power.setVibrationEnable(True)
  power.setVibrationIntensity(50)
  wait_ms(time_ms)
  power.setVibrationEnable(False)

# [Description]
# Shows splash screen when the M5Stack loads
#
# [Parameters]
# screen[M5Screen] : the screen object
#
# [Return]
# None

def splash_screen(screen: M5Screen):
  screen.clean_screen()
  screen.set_screen_bg_color(0xFFFFFF)
  screen.set_screen_brightness(100)

  # Covid Image
  # covid = M5Img("res/covid.png", parent=None)
  # covid.set_align(ALIGN_OUT_BOTTOM_RIGHT, x=64, y=-65, ref=screen.obj)

  # Title
  title = M5Label("M5 COVID-19", color=0x000, font=FONT_MONT_38, parent=None)
  title.set_align(ALIGN_CENTER, x=0, y=-45, ref=screen.obj)

  # Subtitle
  subtitle = M5Label("Covid-19 Alert Program", color=0x777777, font=FONT_MONT_14, parent=None)
  subtitle.set_align(ALIGN_CENTER, x=0, y=-20, ref=screen.obj)

  # Names - START
  names = ["Shehryar Ahmed Subhani", "Juan Diego Guevara", "Ramsha Bilal"]

  y = 20
  for name in names:
    name_label = M5Label(name, color=0x000, font=FONT_MONT_18, parent=None)
    name_label.set_align(ALIGN_CENTER, x=0, y=y, ref=screen.obj)
    y += 20

  # Names - END

  vibrate(50, 1000)
  wait_ms(2000)

# [Description]
# Shows main screen after splash screen
#
# [Parameters]
# screen[M5Screen] : the screen object
#
# [Return]
# None


def main_screen(screen : M5Screen):
  screen.clean_screen()
  screen.set_screen_bg_color(0x000000)
  screen.set_screen_brightness(50)

  dots_counter = 0
  file_counter = 0

  old_time = -1
  old_battery = -1
  old_dots = -1

  while True:
    # Time - START

    if wifiCfg.wlan_sta.isconnected():

      rtc.settime('ntp', host='cn.pool.ntp.org', tzone=4)
      hours = str(rtc.datetime()[4])
      minutes = str(rtc.datetime()[5])

      if len(hours) < 2:
        hours = "0" + hours

      if len(minutes) < 2:
        minutes = "0" + minutes

      time = hours + ":" + minutes

    else:
      time = "00:00"

    # Only update time if it is different (also handles a UIFlow bug where the server occasionally returns 00:00)
    if (time == "03:00" and old_time == "02:59") or (time != old_time and time != "03:00"):
      try:
        time_label.set_hidden(True)
      except:
        pass
      time_label = M5Label(time, color=0xFFFFFF, font=FONT_MONT_20, parent=None)
      time_label.set_align(ALIGN_IN_TOP_RIGHT, x=-10, y=10, ref=screen.obj)
      old_time = time

    # Time - END

    # Battery - START

    is_charging = power.getChargeState()

    if is_charging:
      color = 0x00FF00
    else:
      color = 0xFFFFFF

    battery = map_value((power.getBatVoltage()), 3.7, 4.1, 0, 100)

    if battery <= 20:
      color = 0xFF0000
      if not is_charging:
        vibrate(50, 250)

    if battery != old_battery:
      try:
        battery_label.set_hidden(True)
      except:
        pass
      battery_label = M5Label(str(battery) + "%", color=color, font=FONT_MONT_20, parent=None)
      battery_label.set_align(ALIGN_IN_TOP_LEFT, x=10, y=10, ref=screen.obj)
      old_battery = battery

    # Battery - END


    # Dots and Detection - START

    detection_label = M5Label("DETECTION IN PROGRESS", color=0xFFFFFF, font=FONT_MONT_20, parent=None)
    detection_label.set_align(ALIGN_CENTER, x=0, y=0, ref=screen.obj)

    dots = [".", ".  .  .", ".  .  .  .  ."]

    try:
      dots_label.set_hidden(True)
    except:
      pass
    dots_label = M5Label(dots[dots_counter % 3], color=0xFFFFFF, font=FONT_MONT_30, parent=None)
    dots_label.set_align(ALIGN_CENTER, x=0, y=15, ref=screen.obj)
    old_dots = dots

    dots_counter += 1

    # Dots and Detection - END

    # Recorder - START

    mic.record2file(5, '/sd/audio' + str(file_counter) + ".wav")
    file_counter += 1

    # Recorder - END

    # Survey - START

    screen.clean_screen()
    screen.set_screen_bg_color(0xFFFFFF)
    questions = [
      Question("Do you have a sore throat?"),
      Question("Do you have a dry cough?"),
      Question("Have you experienced loss of taste?"),
      Question("Do you have a fever?"),
      Question("Do you have watery eyes?"),
      Question("Do you have difficulty breathing?"),
      Question("Do you have chest pain?"),
      Question("Do you have muscle pain?"),
      Question("Do you have fatigue?")
      ]

    # Displays each question consecutively
    for question in questions:
      question.display()
      screen.clean_screen()

    screen.clean_screen()
    screen.set_screen_bg_color(0x000000)

    # Survey - END



def main():
  # Initializes screen object
  screen = M5Screen()

  splash_screen(screen)
  main_screen(screen)

if __name__ == "flow.m5cloud":
  main()