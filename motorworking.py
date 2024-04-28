import RPi.GPIO as GPIO
import time

MotorDir = ['forward', 'backward']

ControlMode = ['hardward', 'softward']

class DRV8825():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.mode_pins, GPIO.OUT)

    def digital_write(self, pin, value):
        GPIO.output(pin, value)

    def Stop(self):
        self.digital_write(self.enable_pin, 0)

    def SetMicroStep(self, mode, stepformat):
        microstep = {'fullstep': (0, 0, 0),
                     'halfstep': (1, 0, 0),
                     '1/4step': (0, 1, 0),
                     '1/8step': (1, 1, 0),
                     '1/16step': (0, 0, 1),
                     '1/32step': (1, 0, 1)}

        print("Control mode:", mode)
        if mode == ControlMode[0]:  # Only hardward control
            print("set pins")
            self.digital_write(self.mode_pins, microstep[stepformat])

    def TurnAngle(self, Dir, angle, stepdelay=0.005):
        step_angle = 1.8  # Assuming motor's step angle is 1.8 degrees
        steps = int(angle / step_angle)
        self.TurnStep(Dir, steps, stepdelay)

    def TurnStep(self, Dir, steps, stepdelay=0.005):
        if Dir == MotorDir[0]:
            print("forward")
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 0)
        elif Dir == MotorDir[1]:
            print("backward")
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 1)
        else:
            print("the dir must be: 'forward' or 'backward'")
            self.digital_write(self.enable_pin, 0)
            return

        if steps == 0:
            return

        print("turn step:", steps)
        for i in range(steps):
            self.digital_write(self.step_pin, True)
            time.sleep(stepdelay)
            self.digital_write(self.step_pin, False)
            time.sleep(stepdelay)


try:
    Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

    Motor2.SetMicroStep('hardward', 'halfstep')
    Motor2.TurnAngle(Dir='forward', angle=12)  # Turn by approximately 12 degrees
    Motor2.Stop()

except Exception as e:
    print("An error occurred:", str(e))
    Motor2.Stop()

finally:
    GPIO.cleanup()  # Clean up GPIO

print("\nMotor 2 stopped")
