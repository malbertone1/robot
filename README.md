6WD Robot Project

Hardware
Chassis: Smart 6WD Robot Car Chassis Shock Absorption Kit
Motors: 6x ASLONG DC Motor JGA25-370 12V 500RPM wired in parallel 3 per side
Computing: Raspberry Pi 5 8GB RAM with active cooler and RTC battery
Storage: 256GB SanDisk Ultra A1 microSD
Motor Driver: Cytron MDD10A Dual Channel 10A
Channel 1 Right motors normal polarity
Channel 2 Left motors reversed polarity
LiDAR: RPLIDAR C1 360 degrees USB /dev/ttyUSB0 baudrate 460800
Gyroscope: MPU-6050 GY-521 I2C address 0x68
Camera: Raspberry Pi Camera Module 3 12MP IMX708 CAM/DISP 1 connector
Audio: USB PnP Audio Device hw:2,0 sample rate 44100Hz
Lights: 2x HW-517 MOSFET with 1kohm resistors on signal pins 12V LED strips
Power Motors: LiPo 3S 11.1V 8000mAh Dean T connector via switch to MDD10A
Power Pi5: Anker PowerCore 10K USB-C
Charger: OVONIC Mate1 100W

GPIO Pins
Pin 1 3.3V Gyroscope VCC
Pin 3 SDA Gyroscope SDA
Pin 5 SCL Gyroscope SCL
Pin 6 GND MDD10A signal ground
Pin 9 GND Gyroscope and MOSFET shared ground
Pin 18 GPIO24 MDD10A DIR1 left direction
Pin 22 GPIO25 MDD10A DIR2 right direction
Pin 32 GPIO12 MDD10A PWM1 left speed
Pin 33 GPIO13 MDD10A PWM2 right speed
Pin 36 GPIO16 MOSFET 1 front lights via 1kohm resistor
Pin 38 GPIO20 MOSFET 2 rear lights via 1kohm resistor

Motor Direction
Forward DIR1=0 DIR2=0
Reverse DIR1=1 DIR2=1
Spin clockwise DIR1=0 DIR2=1
Spin counter-clockwise DIR1=1 DIR2=0

Software
OS: Raspberry Pi OS 64-bit Debian Bookworm aarch64
Activate venv: cd robot then source venv/bin/activate
Libraries: gpiozero smbus2 pyrplidar RPi.GPIO
Git: https://github.com/malbertone1/robot.git
Restore: git clone https://github.com/malbertone1/robot.git then cd robot then python3 -m venv venv --system-site-packages then source venv/bin/activate then pip install -r requirements.txt

Config /boot/firmware/config.txt additions
dtparam=i2c_arm=on
dtparam=spi=on
camera_auto_detect=1
dtoverlay=gpio-shutdown

Audio config ~/.asoundrc
defaults.pcm.card 2
defaults.ctl.card 2
Audio config /etc/asound.conf (system wide, survives reboot)
pcm.!default type plug slave pcm type hw card Device rate 44100 channels 2
ctl.!default type hw card Device


Test Scripts
motor_test.py forward and reverse
spin_test.py spinning clockwise and counter-clockwise
gyro_test.py 6-axis gyroscope readings
lidar_test.py full 360 degree scan
mosfet_test.py front and rear lights with dimming

Safety Rules
Initialize GPIO LOW before connecting 12V
Connect battery last after Pi fully booted
Use switch to cut power never unplug battery directly
MOSFET polarity V+ to battery positive V- to battery negative
1kohm resistors on all MOSFET signal pins
Always use sudo poweroff or power button for shutdown

Known Issues and Fixes
RPi.GPIO not compatible with Pi 5 use gpiozero instead
MOSFET reversed polarity causes back-feed fixed with 1kohm resistors and correct polarity
LiDAR rplidar-roboticia incompatible with C1 use pyrplidar with baudrate 460800
Camera not detected use CAM/DISP 1 blue connector near USB-A contacts facing USB-A

Next Steps
Phase 1 main robot.py combining all components COMPLETED
Phase 2 SLAM mapping and room navigation
Phase 3 face recognition and voice greetings
Phase 4 Flask web dashboard
Phase 5 systemd service for autonomous operation
Phase 6 robotic arm future
Phase 7 GPS outdoor navigation future
