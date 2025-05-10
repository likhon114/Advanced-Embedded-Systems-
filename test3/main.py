import GPS,utime,math,LCD
import random
from machine import Pin
import bluetooth
from ble_advertising import advertising_payload
from ble_simple_peripheral import BLESimplePeripheral

ble = bluetooth.BLE()
p = BLESimplePeripheral(ble)

width =480
height=320

center_x=width//2
center_y=height//2
scale=1.5

bck=LCD.RGB(0,0,30)
white=LCD.RGB(250,250,250)
red=LCD.RGB(255,0,0)
green=LCD.RGB(0,200,0)

button15=Pin(15,Pin.IN,Pin.PULL_UP)
button14=Pin(14,Pin.IN,Pin.PULL_UP)
buzzer=Pin(13,Pin.OUT)

def draw_axes():
    LCD.Line(center_x,0,center_x,height,white)  #draw the y-axis line
    LCD.Line(0,center_y,width,center_y,white)
    for i in range(-100,101,10):
        x0,y0=xy_to_pixel(i,-2)
        x1,y1=xy_to_pixel(i,2)
        LCD.Line(x0,y0,x1,y1,white)  #x-axis
       
        x0,y0=xy_to_pixel(-2,i)
        x1,y1=xy_to_pixel(2,i)
        LCD.Line(x0,y0,x1,y1,white)  #y axis
      

def pixel_to_xy(x,y):
    x=(x-center_x)/scale
    y=(center_y-y)/scale
    #print("XY is",x,y)
    return ([x,y])
def xy_to_pixel(x,y):
    pix_X=(center_x+x*scale)
    pix_y=(center_y-y*scale)
    #print("Pixel is ",pix_X,pix_y)
    return ([pix_X,pix_y])


def beep():
    buzzer.on()
    utime.sleep(1)
    buzzer.off()
    utime.sleep(1)

def sethome(self):
    utime.sleep(0.2)
    global current_lat,current_lon,home_lat,home_lon,home_set
    home_lat=current_lat
    home_lon=current_lon
    home_set=True 
   # print("Home location set",home_lat,home_lon)
def pin(self):
    utime.sleep(0.2)
    global counter
    counter= counter+1
    color=LCD.RGB(random.randint(200,255),random.randint(150,255),random.randint(150,255))
    LCD.Text2("*",pix_x,pix_y,green,bck)
    LCD.Circle(pix_x,pix_y,distance*scale,color)
    LCD.Number2(counter,2,0,420,30,red,bck)
    
    
button15.irq(trigger=Pin.IRQ_FALLING,handler=sethome)
button14.irq(trigger=Pin.IRQ_FALLING,handler=pin)


home_lat=None
home_lon=None
home_set=False
game_started=False

home_x=0
home_y=0
pre_x,pre_y=0,0
counter = 0

LCD.Init()
LCD.Clear(bck)
draw_axes()
LCD.Text("Counter",420,10,white,bck)
while True:
    data=GPS.read_data()
    #print(data)
    if data is not None:
        current_lat=(data[0])
        current_lon=(data[1])
        utime.sleep(1)
        if(home_set):
            home_x,home_y=GPS.gps_to_xy(home_lat,home_lon,home_lat,home_lon)
            print("Home XY",home_x,home_y)
            mine_x=random.randint(-100,100)
            mine_y=random.randint(-100,100)
            mine_lat,mine_lon=GPS.xy_to_gps(mine_x,mine_y,home_lat,home_lon)
            link = f"https://www.google.com/maps?q={mine_lat},{mine_lon}"
            p.send(link + "\r\n")
            #print("Mine XY",mine_x,mine_y)
            #print("Mine lat lon",mine_lat,mine_lon)
            distance=math.sqrt(mine_x**2+mine_y**2)
            print("Mine is at ",distance)
            home_set=False
            game_started=True
            #utime.sleep(1)
            
        elif (game_started):
            
            current_x,current_y=GPS.gps_to_xy(current_lat,current_lon,home_lat,home_lon)
            distance=math.sqrt((current_x-mine_x)**2+(current_y-mine_y)**2)
            #print("Distance to mine is",distance)
            #print("Current location",current_x,current_y)
            print("Mine location",mine_lat,mine_lon)
            pix_x,pix_y=xy_to_pixel(current_x,current_y)
            
            LCD.Text2(" ",pre_x,pre_y,bck,bck)
            draw_axes()
            LCD.Text2("+",pix_x,pix_y,white,red)
            pre_x,pre_y=pix_x,pix_y
            #print("previous",pre_x,pre_y)
            
            if(distance<2):
                print("Well done!")
                LCD.Text("Score  ",420,10,white,green)
                beep()
                beep()
            utime.sleep(1)
            
            if p.is_connected():
                
                data = "Location: "+str(current_lat)+","+str(current_lon)+"\nDistance "+str(distance)+"meter"
                p.send(data + "\r\n")
                print("Sent ",data)
                utime.sleep(1)

            
    else:
        print("Check your gps connection")
        utime.sleep(1)



