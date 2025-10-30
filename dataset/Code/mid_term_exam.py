from cs1graphics import *
# http://www.cs1graphics.org/
from cs1graphicsHelper import *
# https://github.com/wellesleycs111/cs1graphicsHelper
from time import sleep
# Pixel Art , Train , Pinky Sunset , Counting stars , little bit dark sky , sun , sea , cloud, steam ...
import random
from PIL import ImageColor

'''
!!! Repl의 Output을 전체화면으로 만들고 실행해주세요 !!!
!!! Output 옆의 [...] 클릭 -> [Maximize] 클릭 !!!

2022010844
컴퓨터과학과 하일환
설명 :
지구로 떨어지는 혜성을 저기 사라진 별의 자리에 되돌려주러 가는 한 기차의 이야기. 

혜성의 순 우리말인 ‘살별’, 평화롭게 바닷가를 거닐던 기차는 지구가 위험에 빠졌다는것을 알게 되고 그 즉시 우주로 향한다. 지구로 떨어지는 살별을 다시 우주로 보내는 긴 여정을 직접 해볼 수 있도록 만들었다.
많은 어려움이 있지만 결국 기차는 살별을 저기 사라진 별의 자리로 되돌리는데 성공한다.

이 애니메이션은 단 한 장의 이미지도 없이 모두 cs1graphics의 함수들로 구성되어있다. 그 중 구름과 산, 바다의 태양 빛 반사, 별자리, 혜성은 애니메이션을 실행 시킬 때 마다 다른 모양으로 만들어져 비슷해 보일 순 있지만, 모든게 완벽하게 똑같은 애니메이션을 다시보는것은 거의 불가능에 가깝다.
혜성을 다시 우주로 향하게 하는 험난한 여정은 섬세한 손길을 요구한다. 단지 반응속도 뿐만이 아닌 예측도 필요하다.

cs1graphics의 자체 성능의 한계로 애니메이션이 느려 보일 수 있습니다. 양해바랍니다.
'''



# = MEMO =
# 1. Canvas
# 2. Layer
# 3. Rectangle
# 4. Circle
# 5. Polygon
# 6. Path
# 7. Text
# 8. Image
# 9. Group
# 10. Animation
# 11. Event
# 12. Color
#   - from PIL import ImageColor
#   - ImageColor.getcolor("#HEXNUM","RGB")
# 13. Point
# 14. Transform
#   - Stars -> (0,0) ~ (0,150)
#   - Moon -> (310,60)
#   - Cloud ->
#   - Sea ->
#   - Train -> (0, 425) ~ (400, 436)
#   - Sun ->
#   - Steam ->
#   - Sky ->
#   - Grass ->
#   - Bridge -> (0,450) ~ (0,600)
#   - Mountain -> (0,400) ~ (0,450)
# 15. Helper


# Main Canvas
canvas = Canvas(400, 600, (119,125,183), 'Midterm Exam - "Comet" - @i1hwan')

# ==== Background ====

# # Clouds
# Clouds = Layer()

# #3F499B #59639E
# # Cloud 1 Generator 63	73	155 (mid) 
# Cloud1 = Layer()
# MidCloud1 = Circle(18)
# MidCloud1.setFillColor(ImageColor.getcolor("#3F499B","RGB"))
# MidCloud1.setBorderWidth(0)  # No border
# Cloud1.add(MidCloud1)
# for i in range(90):
#     cloud = Circle(random.randrange(9, 18))
#     cloud.move(random.randrange(-30, 50), random.randrange(0, 60))
#     cloud.setFillColor(ImageColor.getcolor("#59639E","RGB"))
#     cloud.setBorderWidth(0)  # No border
#     cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
#     Cloud1.add(cloud)

# # Cloud 1 Generator 63	73	155 (side)
# for i in range(60):
#     cloud = Circle(random.randrange(13, 20))
#     cloud.move(random.randrange(-100, 160), random.randrange(45, 89))
#     cloud.setFillColor(ImageColor.getcolor("#8EA3E7","RGB"))
#     cloud.setBorderWidth(0)  # No border
#     cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
#     Cloud1.add(cloud)
    
# Cloud1.scale(random.uniform(0.5, 0.7))
# Clouds.add(Cloud1)


# ==== Cloud Generator ===================================================
#3F499B #59639E
# Cloud 1 Generator 63	73	155 (mid) 
Clouds = Layer()

Cloud1 = Layer()
MidCloud1 = Circle(18)
MidCloud1.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
MidCloud1.setBorderWidth(0)  # No border
Cloud1.add(MidCloud1)

CtCloud1 = Circle(40)
CtCloud1.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
CtCloud1.setBorderWidth(0)  # No border
CtCloud1.move(20, 50)
Cloud1.add(CtCloud1)


for i in range(60):
    cloud = Circle(random.randrange(9, 18))
    cloud.move(random.randrange(-30, 50), random.randrange(0, 60))
    cloud.setFillColor(ImageColor.getcolor("#F0E0E0","RGB"))
    cloud.setBorderWidth(0)  # No border
    cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
    Cloud1.add(cloud)

# Cloud 1 Generator 63	73	155 (side)
for i in range(50):
    cloud = Circle(random.randrange(13, 20))
    cloud.move(random.randrange(-100, 160), random.randrange(45, 89))
    cloud.setFillColor(ImageColor.getcolor("#FEF1DE","RGB"))
    cloud.setBorderWidth(0)  # No border
    cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
    Cloud1.add(cloud)
    
# Cloud 1 Generator (under)
for i in range(30):
    cloud = Circle(random.randrange(4, 15))
    cloud.move(random.randrange(-70, 70), random.randrange(50, 120))
    cloud.setFillColor(ImageColor.getcolor("#FCF5F5","RGB"))
    cloud.setBorderWidth(0)  # No border
    cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
    Cloud1.add(cloud)
    



Cloud1.scale(random.uniform(0.5, 0.7))
Clouds.add(Cloud1) 

# == !! REMOVED BY PERFORMACE ISSUE !! ==
# # Cloud 2 Generator 63	73	155 (mid) 
# Cloud2 = Layer()
# MidCloud2 = Circle(18)
# MidCloud2.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
# MidCloud2.setBorderWidth(0)  # No border
# Cloud2.add(MidCloud2)

# CtCloud2 = Circle(40)
# CtCloud2.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
# CtCloud2.setBorderWidth(0)  # No border
# CtCloud2.move(20, 50)
# Cloud2.add(CtCloud2)

# for i in range(60):
#     cloud = Circle(random.randrange(9, 18))
#     cloud.move(random.randrange(-30, 50), random.randrange(0, 60))
#     cloud.setFillColor(ImageColor.getcolor("#F0E0E0","RGB"))
#     cloud.setBorderWidth(0)  # No border
#     cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
#     Cloud2.add(cloud)

# # Cloud 1 Generator 63	73	155 (side)
# for i in range(50):
#     cloud = Circle(random.randrange(13, 20))
#     cloud.move(random.randrange(-100, 160), random.randrange(45, 89))
#     cloud.setFillColor(ImageColor.getcolor("#FEF1DE","RGB"))
#     cloud.setBorderWidth(0)  # No border
#     cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
#     Cloud2.add(cloud)
    
# # Cloud 1 Generator (under)
# for i in range(30):
#     cloud = Circle(random.randrange(4, 15))
#     cloud.move(random.randrange(-70, 70), random.randrange(50, 120))
#     cloud.setFillColor(ImageColor.getcolor("#FCF5F5","RGB"))
#     cloud.setBorderWidth(0)  # No border
#     cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
#     Cloud2.add(cloud)

# Cloud2.scale(random.uniform(0.3, 0.5))
# Cloud2.move(random.randrange(200, 240), random.randrange(-40, 10))
# Cloud2.flip(180)
# Cloud2.stretch(1, 0.8)
# Clouds.add(Cloud2)

'''
# Cloud 2 Generator 89, 99, 158
for i in range(100):
    cloud = Circle(random.randrange(6, 14))
    cloud.move(random.randrange(-114, 160), random.randrange(72, 130))
    cloud.setFillColor(ImageColor.getcolor("#59639E","RGB"))
    cloud.setBorderWidth(0)  # No border
    Clouds.add(cloud)
    
# Cloud 3 Generator 80,81,140 
for i in range(100):
    cloud = Circle(random.randrange(6, 12))
    cloud.move(random.randrange(-0, 200), random.randrange(115, 148))
    cloud.setFillColor(ImageColor.getcolor("#51518C","RGB"))
    cloud.setBorderWidth(0)  # No border
    Clouds.add(cloud)

# Cloud 4 Generator 157,63,126
for i in range(100):
    cloud = Circle(random.randrange(4, 8))
    cloud.move(random.randrange(-96, 120), random.randrange(136, 185))
    cloud.setFillColor(ImageColor.getcolor("#9D3F7E","RGB"))
    cloud.setBorderWidth(0)  # No border
    Clouds.add(cloud)
'''

# = Moon =
Moon = Layer()
# moon.add(Circle(50).setFillColor((137, 151, 149))) Didn't work right...

moon1 = Circle(30)
moon1.setFillColor((249,255,255))  # Bright side color of moon
moon1.setBorderWidth(0)  # No border
Moon.add(moon1)  # Add to moon layer

moon2 = Circle(30)
moon2.setFillColor((119,125,183))  # Dark side color of moon
moon2.move(7.5,0)
moon2.setBorderWidth(0)  # No border
moon2.stretch(0.85, 1, )  # Shear to make moon look like a moon
Moon.add(moon2)  # Add to moon layer

Moon.rotate(-45)  # Rotate Moon
Moon.move(310, -360)  # Move Moon
Moon.scale(0.7)  # Scale Moon to 50%

# = Stars =
# Star Generator
Stars = Layer()

# Little Star Generator
for i in range(26):
    Star = Layer()
    star = Circle(10);star_ = Circle(10)
    star.stretch(4, 1);star_.stretch(1, 4)
    star.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"));star_.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
    star.setBorderWidth(0);star_.setBorderWidth(0)
    Star.add(star);Star.add(star_)
    Star.scale(random.uniform(0.05, 0.07))
    Star.move(random.randrange(10, 440),random.randrange(-410,320))  # Move Star to random position (Margin 10px)
    Stars.add(Star)

# Big Star Generator
for i in range(8):
    Star = Layer()
    star = Circle(10);star_ = Circle(10)
    star.stretch(4, 1);star_.stretch(1, 4)
    star.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"));star_.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
    star.setBorderWidth(0);star_.setBorderWidth(0)
    Star.add(star);Star.add(star_)
    #Star.rotate(random.randrange(0,360))
    Star.scale(random.uniform(0.07, 0.25))
    Star.move(random.randrange(0, 270),random.randrange(-410,320))  # Move Star to random position (Margin 10px)
    Stars.add(Star)
    
# Comet
# From Particle Generator
class Comet:
    '''
    살별을 여러개 만들기 위해 클래스로 만들었음
    '''
    def __init__(self, x, y, life = 5, size = 0.3, deadSize = 0.8, color = "#FFFFFF"):
        '''
        x, y: 살별이 생성될 좌표 x, y 오프셋 조정 가능함
        life: 살별의 생명 (생명이 0이 되면 살별이 사라짐) (.destroy로 감소)
        size: 살별의 최초 생성 크기
        deadSize: 살별이 사라지는 크기 (1이면 사라지지 않음) (작아지는 속도 조절)
        color: 살별의 색상 hex color
        '''
        self.layer = Layer()
        self.life, self.size, self.deadSize = life, size, deadSize
        self.x, self.y = x, y
        self.c = Circle(10);self.c_ = Circle(10)
        self.c.stretch(4, 1);self.c_.stretch(1, 4)
        self.c.setFillColor(ImageColor.getcolor(color,"RGB"));self.c_.setFillColor(ImageColor.getcolor(color,"RGB"))
        self.c.setBorderWidth(0);self.c_.setBorderWidth(0)
        self.layer.add(self.c);self.layer.add(self.c_)
        self.layer.scale(self.size)
        self.layer.moveTo(x,y)
        self.layer.scale(0.5)
        self.cnt = self.sizeUpCnt = 0
        Background.add(self.layer)
    def drop(self, velX, velY):
        '''
        destroy(self) 호출시 마다 살별의 생명이 1씩 감소, 0보다 작다면 제거 후 True 반환
        '''
        self.layer.moveTo(self.x + velX * self.cnt, self.y + velY * self.cnt)
        self.cnt += 1 + random.randrange(0, 3)
        if not self.life <= 0:
                if not self.sizeUpCnt >= 20:
                    self.layer.scale(1.01)
                    self.sizeUpCnt += 1
                else:
                    self.layer.scale(self.deadSize)  # 작아지는 값 변경 가능
                    self.life -= 1
        else:
            Background.remove(self.layer)
            del self
            return True

comets = {}
comets1 = {}

# ==== Gradient Generator ================================================
# Make a gradient layer
Gradient = Layer()
# Adjustable Variable
offset = 100  # Offset of gradient start point
dense = 30  # You can adjust this value. Make that looks beautiful. bigger -> less dense
palete = (  # You can add more colors. Just add color hex text.
    "#8F7BA3", 
    "#AC749B", 
    "#BC688F", 
    "#D75E88", 
    "#E54A79", 
    "#f16371",
    "#f87c6e",
    "#fc946f",
    "#feac75",
    "#FEB87B", 
    "#feaa6b",
    "#fd9b5c",
    "#fd8b4e",
    "#fc7a43",
    "#FC713E",
    "#AAAAAA"
    )
# Gradient generator
for idx, hex in enumerate(palete):
    gradient_ = Rectangle(400, 400)  # Adjust this with your canvas size.
    gradient_.setFillColor(ImageColor.getcolor(hex,"RGB"))  # Thanks to PIL :)
    gradient_.move(0, idx*dense)
    gradient_.setBorderWidth(0)  # No border
    Gradient.add(gradient_)
# Reset pos & add to canvas
Gradient.move(200, 200 + offset)  # Move a whole Gradient


# = Make A Mountain = #ED553E #810444 #410C42 #190946 #0C0D0B
Mountains = Layer()
mountain = Polygon(Point(20, 458), Point(random.randrange(65, 92), random.randrange(380, 400)), Point(random.randrange(110, 129), random.randrange(394, 427)), Point(random.randrange(147, 159), random.randrange(310, 341)), Point(random.randrange(187, 204), random.randrange(346, 411)), Point(random.randrange(221, 234), random.randrange(407, 421)), Point(random.randrange(237, 251), random.randrange(418, 442)), Point(300, 458))
mountain.setFillColor(ImageColor.getcolor("#ED553E","RGB"))
mountain.setBorderWidth(0)  # No border
# mountain.adjustReference(140, 458)  # Make AnchorPoint to center bottom corner. for make depth color
mountain.adjustReference(120,0)  # Make AnchorPoint to center bottom corner. for make depth color
print(mountain.getReferencePoint())

mountain2 = mountain.clone()  # Create new Mountain front side
mountain2.setFillColor(ImageColor.getcolor("#410C42","RGB"))
# mountain2.scale(0.8)  # Make Depth
mountain2.stretch(1, 0.9) # Make Depth

mountain3 = mountain.clone()  # Create new Mountain front side
mountain3.setFillColor(ImageColor.getcolor("#190946","RGB"))
# mountain3.scale(0.8)  # Make Depth
mountain3.stretch(1, 0.75) # Make Depth

mountain4 = mountain.clone()  # Create new Mountain front side
mountain4.setFillColor(ImageColor.getcolor("#0C0D0B","RGB"))
# mountain4.scale(0.8)  # Make Depth
mountain4.stretch(1, 0.65) # Make Depth

print(mountain.getReferencePoint())
print(mountain2.getReferencePoint())

Mountains.add(mountain)
Mountains.add(mountain2)
Mountains.add(mountain3)
Mountains.add(mountain4)

# TEST
Mountains.move(0, 84) 

# = Sun =
Sun = Layer()
sun = Circle(60)
sun.setBorderWidth(2)
sun.setFillColor(ImageColor.getcolor("#F9FDF4","RGB"))
sun.setBorderColor(ImageColor.getcolor("#FEB77C","RGB"))
sun.move(200, 430)
Sun.add(sun)




# = Seas =
Seas = Layer()
sea_base = Rectangle(400, 200)
sea_base.setBorderWidth(0)  # No border
sea_base.setFillColor(ImageColor.getcolor("#3259A5","RGB"))



# Sea Reflect
# From Gradient maker
Reflect = Layer()
# Adjustable Variable
offset = 33  # Offset of Reflect start point
dense = 5  # You can adjust this value. Make that looks beautiful. bigger -> less dense
circular = 13 # You can adjust this value. Make that looks beautiful.
palete = (  # You can add more colors. Just add color hex text.
    "#5e58aa",
    "#8255aa",
    "#be4c9b",
    "#e84b7c",
    "#fb6054",
    "#FC713E",
    "#fc7a43",
    "#fd8b4e",
    "#fd9b5c",
    "#feaa6b",
    "#FEB87B", 
    "#f9c284",
    "#f5cc90",
    "#efddaa",
    "#eff2d7",
    "#f3f8e6", 
    )
# Reflect generator
for idx, hex in enumerate(palete):
    for x in range(0, len(palete)):
        reflect_ = Rectangle(random.randrange(500 - (offset * idx), 700 - (offset * idx)), dense)  # Adjust this with your canvas size.
        reflect_.setFillColor(ImageColor.getcolor(hex,"RGB"))  # Thanks to PIL :)
        reflect_.move(0, x*dense)
        reflect_.setBorderWidth(0)  # No border
        Reflect.add(reflect_)
# Reset pos & add to canvas
Reflect.move(200, 545)  # Move a whole Reflect
Reflect.stretch(0.4,1)

# # Reflect generator
# for idx, hex in enumerate(palete):
#     reflect_ = Rectangle(200 - (circular * idx), 10)  # Adjust this with your canvas size.
#     reflect_.setFillColor(ImageColor.getcolor(hex,"RGB"))  # Thanks to PIL :)
#     reflect_.move(0, idx*dense)
#     reflect_.setBorderWidth(0)  # No border
#     Reflect.add(reflect_)


# Horizon
Horizon = Rectangle(400, 4)
Horizon.setBorderWidth(0)
Horizon.setFillColor(ImageColor.getcolor("#FEB24E","RGB"))
Horizon.moveTo(200, 540)


Seas.add(sea_base)
Seas.move(200,640)

# ==== Foreground ====

# = Bridge =
B = Layer()
Bridge = Rectangle(1400, 30)
Bridge.moveTo(0, 465)
Bridge.setFillColor('black')
B.add(Bridge)

# Pilar of Bridge
PoB = Layer()
# Pillar width is 30
# pillar = Spline(Point(200,450), Point(220,460), Point(225,480), Point(230,500), Point(230, 600), Point(260, 600), Point(260, 500), Point(265, 480), Point(270, 460), Point(290, 450))

# pillar = Spline(Point(200,450), Point(220,460), Point(225,480), Point(230,500), Point(230, 600), Point(260, 600), Point(260, 500), Point(265, 480), Point(270, 460), Point(290, 450))
# pillar = Spline(Point(200,600), Point(200, 500), Point(230, 450), Point(260, 500), Point(260, 600))
# # pillar = Polygon(Point(200,600), Point(200, 500), Point(230, 450), Point(260, 500), Point(260, 600), Point(290,600), Point(290, 500), Point(320, 450), Point(350, 500), Point(350, 600))
# pillar = Polygon(Point(100, 480), Point(110, 485), Point(115, 490), Point(117, 495), Point(120, 500), Point(120, 600), Point(140, 600), Point(140, 500), Point(143, 495), Point(145 ,490), Point(150 , 485), Point(160, 480))
# pillar.setFillColor('black')

# PoB.add(pillar)
    

for i in range(30):
    pillar = Polygon(Point(100, 480), Point(110, 485), Point(115, 490), Point(117, 495), Point(120, 500), Point(120, 600), Point(140, 600), Point(140, 500), Point(143, 495), Point(145 ,490), Point(150 , 485), Point(160, 480))
    pillar.move(-70*i, 0)
    pillar.setFillColor('black')    
    PoB.add(pillar)
    

# = Train =
Trains = Layer()
# Main Train
MTrain = Layer()

train_main = Rectangle(60, 26)
train_main.setBorderWidth(0)  # No border
train_main.setFillColor(ImageColor.getcolor("#190A09","RGB"))
train_main.move(0,1)

train_mainUpper = Rectangle(50, 10)
train_mainUpper.setBorderWidth(0)  # No border
train_mainUpper.setFillColor(ImageColor.getcolor("#190A09","RGB"))
train_mainUpper.move(0, -10)

train_mainWindow = Rectangle(25,7)
train_mainWindow.setBorderWidth(0)  # No border
train_mainWindow.setFillColor(ImageColor.getcolor("#FDA22B","RGB"))
train_mainWindow.move(-16, -3)

train_mainWindow_ = train_mainWindow.clone()
train_mainWindow_.move(29, 0)


MTrain.add(train_main);MTrain.add(train_mainUpper);MTrain.add(train_mainWindow);MTrain.add(train_mainWindow_)

MTrain.move(130, 436)



Trains.add(MTrain)
# Train Cabin Generator

for i in range(3):  # Make N Train Cabins. You can adjust this value to make more or less cabins.
    Train = Layer()
    train_cabin = Rectangle(70, 25);train_cabin_ = Rectangle(70, 25);train_cabin__ = Rectangle(70, 25)
    train_cabin.setFillColor(ImageColor.getcolor("#410D42","RGB")) #410D42  # Set Cabin Color
    train_cabin_.setFillColor(ImageColor.getcolor("#190946","RGB")) #190946  # Set Cabin Color
    train_cabin__.setFillColor(ImageColor.getcolor("#190A09","RGB")) #090A09  # Set Cabin Color
    train_cabin_.stretch(1, 0.90);train_cabin__.stretch(1, 0.9) # Make Depth
    train_cabin_.move(0,1);train_cabin__.move(0,3)  # Make Depth
    train_window = Rectangle(17, 7)
    train_window.setFillColor(ImageColor.getcolor("#FDA22B","RGB"))  # Set Window Color
    train_window.move(-20,-3)
    train_window_ = train_window.clone()
    train_window_.move(20,0)
    train_window__ = train_window_.clone()
    train_window__.move(20,0)
    train_connectingRod = Rectangle(5, 5)
    train_connectingRod.setFillColor(ImageColor.getcolor("#190A09","RGB"))  # Set Connecting Rod Color
    train_connectingRod.move(-38, 8)
    # No Border
    train_cabin.setBorderWidth(0);train_cabin_.setBorderWidth(0);train_cabin__.setBorderWidth(0)
    train_window.setBorderWidth(0);train_window_.setBorderWidth(0);train_window__.setBorderWidth(0)
    train_connectingRod.setBorderWidth(0)
    # Add to Train Layer
    Train.add(train_cabin);Train.add(train_cabin_);Train.add(train_cabin__)
    Train.add(train_window);Train.add(train_window_);Train.add(train_window__)
    Train.add(train_connectingRod)
    Train.move(200 + (75 * i), 436)  # move For make N trains
    Trains.add(Train) # Add to Trains Layer


# = Steam =



# == Zoom in to train ==
# == inside of train ==




# === Add layer to canvas ===
Background = Layer()
Foreground = Layer()

Background.add(Gradient)
Background.add(Sun)
Background.add(Stars)
Background.add(Moon)
Background.add(Seas)
Background.add(Horizon)
Background.add(Reflect)
Background.add(Mountains)
Background.add(Clouds)
Foreground.add(PoB)
Foreground.add(B)
Foreground.add(Trains)


canvas.add(Background)
canvas.add(Foreground)





# Position Reset
Clouds.move(100,330)
PoB.move(300,0)

# Test
Moon.move(0, -100)
Stars.move(0,-100)

# Zoom test ( NOT WORK PROPERLY )
# canvas.zoomView(50, Point(114,434))

# for i in range(50):
#     canvas.zoomView(0.9, Point(114,434))
#     sleep(0.01)


# 도대체 이벤트랑 이벤트 핸들러는 어떻게 쓰는거야 ;;
# evt = Event()
# evthandler = EventHandler()
# evthandler.handle(evt)


# # TEXT
# Txt = Text()
# Txt.setMessage("Hello World")
# canvas.add(Txt)
# Txt.addHandler(evthandler)

# # = Helper =


j = c2022yh = cnt2022yh = c9 = cnt9 = 0

# =  1. Animation =  ( PERFORMANCE OPTIMIZED )
for i in range(350):
    PoB.move(2, 0)
    # if i % 100 == 0:
    #     Clouds.move(1,0)
    Mountains.move(0.1, 0)
    Sun.move(0.002,0)
    Reflect.move(0.002,0)
    # if i % 50 == 0:
    if i >= 200:
        Trains.move(-(0.001 + (0.01 * j * j)), 0)
        j += 1

    if c2022yh == cnt2022yh:
        comets["comets{0}".format(c2022yh)] = Comet(random.randrange(160, 450),random.randrange(-20, 40),15, 0.27, 0.9)
        cnt2022yh += 1  # 살별 중복 생성 방지
    if comets["comets{0}".format(c2022yh)].drop(-2, 1) == True:  # 살별 생명 감소 및 삭제
        c2022yh += 1  # 다음 살별로 넘어가기
    if c9 == cnt9:
        comets1["comets{0}".format(c9)] = Comet(random.randrange(40, 350),random.randrange(20, 130),7, 0.11, 0.9)
        cnt9 += 1  # 살별 중복 생성 방지
    if comets1["comets{0}".format(c9)].drop(-1, 1) == True:  # 살별 생명 감소 및 삭제
        c9 += 1  # 다음 살별로 넘어가기
    sleep(0.01)
    
# # Try to delete comets
# try:
#     canvas.remove(comets["comets{0}".format(c2022yh)])
#     print(f"Success: Delete comets in canvas c2022yh")
# except:
#     print(f"Error: No comets in canvas c2022yh")
#     pass

# try:
#     canvas.remove(comets1["comets{0}".format(c9)])
#     print(f"Success: Delete comets in canvas c9")
# except:
#     print(f"Error: No comets in canvas c9")
#     pass

# try:
#     canvas.remove(comets["comets{0}".format(c2022yh - 1)])
#     print(f"Success: Delete comets in canvas c2022yh - 1")
# except:
#     print(f"Error: No comets in canvas c2022yh - 1")
#     pass

# try:
#     canvas.remove(comets1["comets{0}".format(c9 - 1)])
#     print(f"Success: Delete comets in canvas c9 - 1")
# except:
#     print(f"Error: No comets in canvas c9 - 1")
#     pass

# try:
#     canvas.remove(comets["comets{0}".format(c2022yh + 1)])
#     print(f"Success: Delete comets in canvas c2022yh + 1")
# except:
#     print(f"Error: No comets in canvas c2022yh + 1")
#     pass

# try:
#     canvas.remove(comets1["comets{0}".format(c9 + 1)])
#     print(f"Success: Delete comets in canvas c9 + 1")
# except:
#     print(f"Error: No comets in canvas c9 + 1")
#     pass

# Transition (PERFORMANCE OPTIMIZED)
for i in range(250):
    if c2022yh == cnt2022yh:
        comets["comets{0}".format(c2022yh)] = Comet(random.randrange(160, 450),random.randrange(-20, 40),15, 0.27, 0.9)
        cnt2022yh += 1  # 살별 중복 생성 방지
    if comets["comets{0}".format(c2022yh)].drop(-2, 1) == True:  # 살별 생명 감소 및 삭제
        c2022yh += 1  # 다음 살별로 넘어가기
    if c9 == cnt9:
        comets1["comets{0}".format(c9)] = Comet(random.randrange(40, 350),random.randrange(20, 130),7, 0.11, 0.9)
        cnt9 += 1  # 살별 중복 생성 방지
    if comets1["comets{0}".format(c9)].drop(-1, 1) == True:  # 살별 생명 감소 및 삭제
        c9 += 1  # 다음 살별로 넘어가기
    Background.move(0,2)
    Foreground.move(0,4)
    # sleep(0.01) waht? lag
    
# 최적화
Background.remove(Gradient)
Background.remove(Sun)
Background.remove(Seas)
Background.remove(Mountains)
Background.remove(Clouds)
Background.remove(Horizon)
Background.remove(Reflect)
canvas.remove(Foreground)


################################################################
# ######## BRICKOUT GAME START##### ############################
################################################################

# 초기 변수 세팅 
Velocity = -4  # 이 변수를 조정해서 공의 속도와 초기 방향을 조정
Margin = 20 # 그만좀 튀어나가 ㅠㅠ
leftWall, rightWall, topWall, bottomWall = 0 + Margin, 400 - Margin, 0 + Margin, 600 - Margin  # 캔버스 사이즈와 공의 CenterPt에 맞추어 조정

# Player Setting ====
player = Rectangle(130, 28) # Center pt = 68, 14  # 히트박스 수정
player.setBorderWidth(0)  # No border
player.move(200,450)  # Pos reset

# Ball Setting ====
ball = Circle(10)  # Center pt = 5, 5  # 히트박스가 안맞는 문제로 10을 7로 변경
b_Xpos, b_Ypos = 200, 400  # For ball pos reset
b_Xvel, b_Yvel = Velocity, Velocity  # For ball velocity reset
ball.move(-b_Xpos, -b_Ypos)  # Pos reset start to left up side
ball.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
ball.setBorderWidth(0)  # No border


# Ball Trail (Particle) =============================
# Particle Maker - From Star Generator
class Particle:
    '''
    파티클을 여러개 만들기 위해 클래스로 만들었음
    '''
    def __init__(self, x, y, life = 5, size = 0.3, deadSize = 0.8, color = "#FFFFFF"):
        '''
        x, y: 파티클이 생성될 좌표 x, y 오프셋 조정 가능함
        life: 파티클의 생명 (생명이 0이 되면 파티클이 사라짐) (.destroy로 감소)
        size: 파티클의 최초 생성 크기
        deadSize: 파티클이 사라지는 크기 (1이면 사라지지 않음) (작아지는 속도 조절)
        color: 파티클의 색상 hex color
        '''
        self.layer = Layer()
        self.life, self.size, self.deadSize = life, size, deadSize
        self.c = Circle(10);self.c_ = Circle(10)
        self.c.stretch(4, 1);self.c_.stretch(1, 4)
        self.c.setFillColor(ImageColor.getcolor(color,"RGB"));self.c_.setFillColor(ImageColor.getcolor(color,"RGB"))
        self.c.setBorderWidth(0);self.c_.setBorderWidth(0)
        self.layer.add(self.c);self.layer.add(self.c_)
        self.layer.scale(self.size)
        self.layer.moveTo(x,y)
        canvas.add(self.layer)
    def destroy(self):
        '''
        destroy(self) 호출시 마다 파티클의 생명이 1씩 감소, 0보다 작다면 제거 후 True 반환
        '''
        if not self.life <= 0:
            self.layer.scale(self.deadSize)  # 작아지는 값 변경 가능
            self.life -= 1
        else:
            canvas.remove(self.layer)
            del self
            return True

particles1 = {}
particles2 = {}
particles3 = {}

# Plife = 5
# def Particle(x, y, life, size):
#     if Plife <= 0:
#         particleLife, particleSize = life, size
#         Particle = Layer()
#         particle = Circle(10);particle_ = Circle(10)
#         particle.stretch(4, 1);particle_.stretch(1, 4)
#         particle.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"));particle_.setFillColor(ImageColor.getcolor("#FFFFFF","RGB"))
#         particle.setBorderWidth(0);particle_.setBorderWidth(0)
#         Particle.add(particle);Particle.add(particle_)
#         Particle.scale(particleSize)
#         Particle.moveTo(x,y)
#         canvas.add(Particle)
        
# def ParticleRemove(particle):
#     Plife -= 1
    
#         for i in sorted(range(1, particleLife + 1), reverse=True):
#             Star.scale((particleSize / i))
#         canvas.remove(Star)
# Brick Setting ====
# Old Code
# brick = Rectangle(60, 20) # Center pt = 30, 10
# brick.setFillColor('blue')
# brick.move(200, 100)  # Pos reset
# print(brick.getReferencePoint())


# Brick Generator =================
# 초기 변수 세팅
BrickX = 60  # Brick X 크기
BrickY = 25  # Brick Y 크기
SpaceX = 60  # Brick 간의 X축 간격
SpaceY = 30  # Brick 간의 Y축 간격

brickCoordinates = [  # Brick의 좌표를 저장할 리스트 -> 갯수 정하면 자동으로 생성되게 만들 수 있을듯
[200 - SpaceX * 2,100 + SpaceY * 0], [200 - SpaceX * 1,100 + SpaceY * 0], [200,100 + SpaceY * 0], [200 + SpaceX * 1,100 + SpaceY * 0], [200 + SpaceX * 2,100 + SpaceY * 0],
[200 - SpaceX * 2,100 + SpaceY * 1], [200 - SpaceX * 1,100 + SpaceY * 1], [200,100 + SpaceY * 1], [200 + SpaceX * 1,100 + SpaceY * 1], [200 + SpaceX * 2,100 + SpaceY * 1],
[200 - SpaceX * 2,100 + SpaceY * 2], [200 - SpaceX * 1,100 + SpaceY * 2], [200,100 + SpaceY * 2], [200 + SpaceX * 1,100 + SpaceY * 2], [200 + SpaceX * 2,100 + SpaceY * 2]
]

'''
Brick Coordinate
(Center)
[            |-20-|       |-20-|         |-20-|         |-20-|                 
    |(100,100)  |  (150,100)  |  (200, 100)  |  (250, 100)  |  (300, 100)
 10 |        |-20-|       |-20-|         |-20-|         |-20-|
    |(100,120)  |  (150,120)  |  (200, 120)  |  (250, 120)  |  (300, 120)
 10 |        |-20-|       |-20-|         |-20-|         |-20-|
    |(100,140)  |  (150,140)  |  (200, 140)  |  (250, 140)  |  (300, 140)
]
벽돌 틈 사이즈는 20
벽돌 가로 사이즈는 60 세로 사이즈는 20
가운데로부터 각각 +-30, +-10이 테두리
조정 가능함
'''

# Brick Generator =================
# Brick Painter - From Gradient Generator
palete = (  # You can add more colors. Just add color hex text.
    "#937DC2", 
    "#937DC2", 
    "#937DC2", 
    "#937DC2", 
    "#937DC2",
    "#C689C6",
    "#C689C6",
    "#C689C6", 
    "#C689C6",
    "#C689C6",
    "#E8A0BF",
    "#E8A0BF",
    "#E8A0BF",
    "#E8A0BF",
    "#E8A0BF",
    "#E8A0BF"
    )

bricks = {}  # Thx to StackOverflow
for idx, pos in enumerate(brickCoordinates):  # Clone Brick With Addressed Coordinates
    bricks["brick{0}".format(idx)] = Rectangle(BrickX - 10, BrickY - 5) # Center pt = 30, 10  # 히트박스 보정을 위해 좌표보다 작게 보임
    bricks["brick{0}".format(idx)].setFillColor(ImageColor.getcolor(palete[idx],"RGB"))  # Set Color
    bricks["brick{0}".format(idx)].setBorderColor(ImageColor.getcolor("#FFFFFF","RGB"))  # Set Border Color
    bricks["brick{0}".format(idx)].move(pos[0], pos[1])  # Pos reset
    canvas.add(bricks["brick{0}".format(idx)])  # Make Variable in loop. Thx to StackOverflow
    # https://stackoverflow.com/questions/6181935/how-do-you-create-different-variable-names-while-in-a-loop
    # print(f"[DEBUG] {brick.getReferencePoint()})
# print(f"[DEBUG] {bricks}"")

for i in bricks:
    print(f"[DEBUG] {i} : {bricks[i].getReferencePoint()}")
    
# 벽돌 좌표를 리스트 써서 저장해놓고, 공이 벽돌에 닿으면 리스트에서 빼내서 삭제하는 방식으로 구현
# 벽돌을 여러개 만들고 한번에 관리가 가능할까?
# 벽돌은 무조건 100x20 사이즈로 만들고, 위치만 조정해서 여러개 만들어서 관리하는 방식으로 구현

# Add to canvas
canvas.add(ball)
# canvas.add(brick)  # Add brick to canvas
canvas.add(player)  # Add player to canvas

# TRAIN
# Main Train -> Player
Trains = Layer()
MTrain = Layer()

train_main = Rectangle(60, 26)
train_main.setBorderWidth(0)  # No border
train_main.setFillColor(ImageColor.getcolor("#190A09","RGB"))
train_main.move(0,1)
train_mainUpper = Rectangle(50, 10)
train_mainUpper.setBorderWidth(0)  # No border
train_mainUpper.setFillColor(ImageColor.getcolor("#190A09","RGB"))
train_mainUpper.move(0, -10)
train_mainWindow = Rectangle(25,7)
train_mainWindow.setBorderWidth(0)  # No border
train_mainWindow.setFillColor(ImageColor.getcolor("#FDA22B","RGB"))
train_mainWindow.move(-16, -3)
train_mainWindow_ = train_mainWindow.clone()
train_mainWindow_.move(29, 0)
MTrain.add(train_main);MTrain.add(train_mainUpper);MTrain.add(train_mainWindow);MTrain.add(train_mainWindow_)
MTrain.move(130, 436)
Trains.add(MTrain)

# 메인 기차와 한량만 추가
Train = Layer()
train_cabin = Rectangle(70, 25);train_cabin_ = Rectangle(70, 25);train_cabin__ = Rectangle(70, 25)
train_cabin.setFillColor(ImageColor.getcolor("#410D42","RGB")) #410D42  # Set Cabin Color
train_cabin_.setFillColor(ImageColor.getcolor("#190946","RGB")) #190946  # Set Cabin Color
train_cabin__.setFillColor(ImageColor.getcolor("#190A09","RGB")) #090A09  # Set Cabin Color
train_cabin_.stretch(1, 0.90);train_cabin__.stretch(1, 0.9) # Make Depth
train_cabin_.move(0,1);train_cabin__.move(0,3)  # Make Depth
train_window = Rectangle(17, 7)
train_window.setFillColor(ImageColor.getcolor("#FDA22B","RGB"))  # Set Window Color
train_window.move(-20,-3)
train_window_ = train_window.clone()
train_window_.move(20,0)
train_window__ = train_window_.clone()
train_window__.move(20,0)
train_connectingRod = Rectangle(5, 5)
train_connectingRod.setFillColor(ImageColor.getcolor("#190A09","RGB"))  # Set Connecting Rod Color
train_connectingRod.move(-38, 8)
# No Border
train_cabin.setBorderWidth(0);train_cabin_.setBorderWidth(0);train_cabin__.setBorderWidth(0)
train_window.setBorderWidth(0);train_window_.setBorderWidth(0);train_window__.setBorderWidth(0)
train_connectingRod.setBorderWidth(0)
# Add to Train Layer
Train.add(train_cabin);Train.add(train_cabin_);Train.add(train_cabin__)
Train.add(train_window);Train.add(train_window_);Train.add(train_window__)
Train.add(train_connectingRod)
Train.move(200, 436)  # move For make N trains
Trains.add(Train) # Add to Trains Layer

# Train이 옆에서 나오는 모션 연출
Trains.moveTo(0,0)
canvas.add(Trains)
Trains.adjustReference(168, 436)
Trains.moveTo(468,450)
for i in range(100):
    Trains.move(-1,0)
    sleep(0.01)
# /TRAIN

# Messages
txt_click = Text("Click Train to Start", 20)
txt_click.setFontColor(ImageColor.getcolor("#BDC3FF","RGB"))
txt_click.moveTo(200, 500)
canvas.add(txt_click)

Trains.wait()  # Wait for Clicking Player


# Reset Variables
Score = 0
Life = 3
RandomMin = 1  # 일반화된 회전각도를 없애기 위해 랜덤값을 더해줌
RandomMax = 2  # 일반화된 회전각도를 없애기 위해 랜덤값을 더해줌 -> 대신 벽에 닿을때 마진을 늘려야함
Velocity_Accel = 1  # 재미를 위해 공의 속도를 점점 빠르게 만들어주는 변수 -> 에러가 너무 나서 못쓰겠음
Xcnt = 5 # 에러 수정용
Ycnt = 5 # 에러 수정용
Pcnt = 5 # 에러 수정용
Bcnt = 5 # 에러 수정용
X = 0 # TEST
Y = 1 # TEST
p1 = p2 = p3 = 0 # Particle test
cnt1 = cnt2 = cnt3 = 0 # Particle test
win = False

txt_life = Text("Life : " + str(Life), 15)
txt_life.setFontColor(ImageColor.getcolor("#3A3F6B","RGB"))
txt_life.moveTo(200, 520)
canvas.add(txt_life)
canvas.setAutoRefresh(True)  # Auto Refresh 함수를 찾긴 했는데 정확히 뭐하는건지는 모르겠음.

while True:  # Do Forever
    # Score Set ===
    txt_click.setMessage("Score: " + str(Score))  # 점수 표시로 변환
    txt_life.setMessage("Life: " + str(Life))  # 생명 표시
    # Player Move ===
    PlayerX = canvas.getMouseCoordinates().getX()  # 마우스 X좌표 저장
    PlayerY = 450  # Player Y좌표 고정
    player.moveTo(PlayerX, PlayerY)  # 마우스 좌표에 따라 플레이어 이동
    Trains.moveTo(PlayerX, PlayerY)  # Move Sprite
    # print(f"[DEBUG] Mouse:{canvas.getMouseCoordinates()} b_Xpos:{b_Xpos} b_Ypos:{b_Ypos} b_Xvel:{b_Xvel} b_Yvel:{b_Yvel} vel:{Velocity}")
    
    # Ball Particles  ====
    # Particle 1
    # Particle(b_Xpos,b_Ypos,5, 1)
    if p1 == cnt1:
        particles1["particles{0}".format(p1)] = Particle(b_Xpos,b_Ypos,10, 0.24, 0.9)
        cnt1 += 1  # 파티클 중복 생성 방지
    # if particles["particles{0}".format(i)].life <= 0:  # 파티클 생명이 0일 경우
    #     p += 1  # 다음 파티클로 넘어가기
    if particles1["particles{0}".format(p1)].destroy() == True:  # 파티클 생명 감소 및 삭제
        p1 += 1  # 다음 파티클로 넘어가기
    # Particle 2
    if p2 == cnt2:
        particles2["particles{0}".format(p2)] = Particle(b_Xpos+1,b_Ypos-1,15, 0.2, 0.94)
        cnt2 += 1  # 파티클 중복 생성 방지
    if particles2["particles{0}".format(p2)].destroy() == True:  # 파티클 생명 감소 및 삭제
        p2 += 1  # 다음 파티클로 넘어가기
    # # Particle 3 (Performance Issue)
    # if p3 == cnt3:
    #     particles3["particles{0}".format(p3)] = Particle(b_Xpos-3,b_Ypos+4,7, 0.1, 0.4)
    #     cnt3 += 1  # 파티클 중복 생성 방지
    # if particles3["particles{0}".format(p3)].destroy() == True:  # 파티클 생명 감소 및 삭제
    #     p3 += 1  # 다음 파티클로 넘어가기
        
    # Ball Move ===
    ball.moveTo(b_Xpos, b_Ypos)  # 공의 움직임 반영
        
    # X-axis
    b_Xpos += b_Xvel # X축 속도에 가속값을 더해줌
    if (b_Xpos <= leftWall or b_Xpos >= rightWall) and Xcnt == 0:  # 만약 공이 벽에 닿았을 경우
        Xcnt = 5  # 에러 수정용
        b_Xvel = -b_Xvel  # 공의 가속도 반전
        Velocity += Velocity_Accel  # 공의 속도 증가
    # Y-axis
    b_Ypos += b_Yvel  # Y축 속도에 가속값을 더해줌
    if (b_Ypos <= topWall) and Ycnt == 0:  # 만약 공이 벽에 닿았을 경우
        Ycnt = 5  # 에러 수정용
        b_Yvel = -b_Yvel # 공의 가속도 반전
        Velocity += Velocity_Accel  # 공의 속도 증가
    if (b_Ypos >= bottomWall) and Ycnt == 0:
        Ycnt = 5
        Life -= 1
        b_Xpos = b_Ypos =  250
        if Life <= 0:
            break
        
    # Trying to Catch Exception
    if b_Ypos >= bottomWall + Margin or b_Ypos <= topWall - Margin or b_Xpos >= rightWall + Margin or b_Xpos <= leftWall - Margin:
        print(f"[DEBUG] Exception Occured")
        ball.moveTo(250, 250)
        b_Xvel, b_Yvel = 0, 0
        Velocity = 1
        quit()
        
    
    
    # Hit brick
    for idx, pos in enumerate(brickCoordinates):  # Special Thanks to Github Copilot
        if Bcnt == 0:
            if (pos[0] - (BrickX / 2) <= b_Xpos <= pos[0] + (BrickX / 2)):
                if (pos[1] - (BrickY / 2) <= b_Ypos <= pos[1] + (BrickY / 2)):
                    Bcnt = 5
                    for i in bricks:
                            print(f"[DEBUG] {i} : {bricks[i].getReferencePoint()}")
                    print(f"[DEBUG] Hit Brick idx:{idx} pos:{pos} :{brickCoordinates} len{len(brickCoordinates)}")
                    b_Yvel = -(b_Yvel)# 가속도 반전
                    # bricks["brick{0}".format(idx)].setBorderWidth(0)  # Canvas에서 벽돌 제거 <- 여기 뭔가 문제가 있음
                    # bricks["brick{0}".format(idx)].setFillColor('transparent')  # Canvas에서 벽돌 제거
                    # try:
                    #     canvas.remove(bricks["brick{0}".format(idx)])  # Canvas에서 벽돌 제거
                    # except:
                    #     for i in bricks:
                    #         print(f"[DEBUG] {i} : {bricks[i].getReferencePoint()}")
                    brickCoordinates[idx] = (-1,-1) # 벽돌의 좌표로 공이 닿았는지 확인하므로 닿은 이후에는 제거
                    canvas.remove(bricks["brick{0}".format(idx)]) # 벽돌의 좌표로 공이 닿았는지 확인하므로 닿은 이후에는 제거
                    print(f"[DEBUG] :{brickCoordinates} len: {len(brickCoordinates)}")
                    Velocity += Velocity_Accel  # 공의 속도 증가
                    Score += 1  # 점수 추가
                    print(f"Score:{Score}")  # 점수 출력
                    break  # 반복문 탈출
            elif (pos[1] - (BrickY / 2) <= b_Ypos <= pos[1] + (BrickY / 2)):  # 공이 벽돌에 닿았을 경우 (좌표리스트 전부 확인) -> (최적화 필요)
                if (pos[0] - (BrickX / 2) <= b_Xpos <= pos[0] + (BrickX / 2)):
                    Bcnt = 5
                    for i in bricks:
                            print(f"[DEBUG] {i} : {bricks[i].getReferencePoint()}")
                    print(f"[DEBUG] Hit Brick idx:{idx} pos:{pos} :{brickCoordinates} len{len(brickCoordinates)}")
                    b_Xvel = -(b_Xvel)# 가속도 반전
                    # bricks["brick{0}".format(idx)].setBorderWidth(0)  # Canvas에서 벽돌 제거 <- 여기 뭔가 문제가 있음
                    # bricks["brick{0}".format(idx)].setFillColor('transparent')  # Canvas에서 벽돌 제거
                    # try:
                    #     canvas.remove(bricks["brick{0}".format(idx)])  # Canvas에서 벽돌 제거
                    # except:
                    #     for i in bricks:
                    #         print(f"[DEBUG] {i} : {bricks[i].getReferencePoint()}")
                    brickCoordinates[idx] = (-1,-1) # 벽돌의 좌표로 공이 닿았는지 확인하므로 닿은 이후에는 제거
                    canvas.remove(bricks["brick{0}".format(idx)]) # 벽돌의 좌표로 공이 닿았는지 확인하므로 닿은 이후에는 제거
                    print(f"[DEBUG] :{brickCoordinates} len: {len(brickCoordinates)}")
                    Velocity += Velocity_Accel  # 공의 속도 증가
                    Score += 1  # 점수 추가
                    print(f"Score:{Score}")  # 점수 출력
                    break  # 반복문 탈출
    # if b_Xpos == brick.getReferencePoint().getX() and b_Ypos == brick.getReferencePoint().getY():  # 만약 공이 벽돌에 닿았을 경우
    
    # Hit player (fixed value)
    if (PlayerX - 68 <= b_Xpos <= PlayerX + 68) and (PlayerY - 14 <= b_Ypos <= PlayerY + 14) and Pcnt == 0:
        if PlayerX < 200:  # Player가 왼쪽에 있을 경우
            b_Xvel = -b_Xvel  # 가속도 반전
        b_Yvel = -b_Yvel  # 가속도 반전
        Velocity += Velocity_Accel  # 공의 속도 증가
        print("[DEBUG] Hit player")
    
    # 에러 수정용
    Xcnt = 0 if Xcnt == 0 else Xcnt - 1
    Ycnt = 0 if Ycnt == 0 else Ycnt - 1
    Pcnt = 0 if Pcnt == 0 else Pcnt - 1
    Bcnt = 0 if Bcnt == 0 else Bcnt - 1
    # Win Game ===
    if Score >= 15:  # 100점 넘을시 종료
        win = True
        break
    # Velocity += 0.1  # 공의 속도 증가
    sleep(0.001)
    
if win == True:
    txt_life.setMessage("You Win!")
else:
    txt_life.setMessage("Game Over!")




'''
@TODO: 벽돌 부딫히는 부분 입사 반사각으로 변경
-> https://ai-creator.tistory.com/534
대각선으로 완만하게 나갈때 벽 판정에서 오류가 발생함
-> 수정 완료 (속도 높이면 다시 나갈수도..)
@TODO: 배경 별 반짝이게 만들기
@TODO: 


'''


'''
for idx,pos in enumerate(brickCoordinates):  
    brick = Rectangle(60, 20) # Center pt = 30, 10
    brick.setFillColor('blue')
    print(f"Brick {idx} : {pos} ")
    brick.move(pos[idx][0], pos[idx][1])  # Pos reset
    print(brick.getReferencePoint())

pos[idx][0]을 찾으면
int형변환 관련 에러가 나고
pos[idx]를 찾으면
인덱스 에러가 났음

C스타일로 코드를 짜다보니 이렇게 되는건지 잘 몰랐었는데
그냥 pos[0] pos[1] 이렇게 하면 됨
enumerate를 쓰면 pos에 brickCoordinates의 2차원 리스트중 1차원 원소가 들어가는듯

'''


# Code Archive
'''
# Clouds
Clouds = Layer()

# Cloud 1 Generator 63	73	155 (mid)
Cloud1 = Layer()
MidCloud1 = Circle(18)
MidCloud1.setFillColor(ImageColor.getcolor("#3F499B","RGB"))
MidCloud1.setBorderWidth(0)  # No border
Cloud1.add(MidCloud1)
for i in range(90):
    cloud = Circle(random.randrange(9, 18))
    cloud.move(random.randrange(-30, 50), random.randrange(0, 60))
    cloud.setFillColor(ImageColor.getcolor("#3F499B","RGB"))
    cloud.setBorderWidth(0)  # No border
    cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
    Cloud1.add(cloud)

# Cloud 1 Generator 63	73	155 (side)
for i in range(60):
    cloud = Circle(random.randrange(13, 20))
    cloud.move(random.randrange(-100, 160), random.randrange(45, 89))
    cloud.setFillColor(ImageColor.getcolor("#3F499B","RGB"))
    cloud.setBorderWidth(0)  # No border
    cloud.move(random.randrange(-50, 50), random.randrange(-10, 10))  # Make Position random
    Cloud1.add(cloud)

Cloud1.scale(0.7)
Clouds.add(Cloud1)
'''
    
# Code Archive - Make Mountain
'''
# = Make A Mountain = #ED553E #810444 #410C42 #190946 #0C0D0B
Mountains = Layer()
mountain = Polygon(Point(20, 458), Point(random.randrange(65, 92), random.randrange(380, 400)), Point(random.randrange(110, 129), random.randrange(394, 447)), Point(random.randrange(147, 159), random.randrange(370, 450)), Point(random.randrange(187, 204), random.randrange(388, 411)), Point(random.randrange(221, 234), random.randrange(407, 421)), Point(random.randrange(237, 251), random.randrange(418, 442)), Point(300, 458))
mountain.setFillColor(ImageColor.getcolor("#ED553E","RGB"))
mountain.setBorderWidth(0)  # No border
# mountain.adjustReference(140, 458)  # Make AnchorPoint to center bottom corner. for make depth color
mountain.adjustReference(120,0)  # Make AnchorPoint to center bottom corner. for make depth color
print(mountain.getReferencePoint())


mountain2 = mountain.clone()  # Create new Mountain front side
mountain2.setFillColor(ImageColor.getcolor("#410C42","RGB"))
# mountain2.scale(0.8)  # Make Depth
mountain2.stretch(1, 0.9) # Make Depth

mountain3 = mountain.clone()  # Create new Mountain front side
mountain3.setFillColor(ImageColor.getcolor("#190946","RGB"))
# mountain3.scale(0.8)  # Make Depth
mountain3.stretch(1, 0.75) # Make Depth

mountain4 = mountain.clone()  # Create new Mountain front side
mountain4.setFillColor(ImageColor.getcolor("#0C0D0B","RGB"))
# mountain4.scale(0.8)  # Make Depth
mountain4.stretch(1, 0.65) # Make Depth

print(mountain.getReferencePoint())
print(mountain2.getReferencePoint())

Mountains.add(mountain)
Mountains.add(mountain2)
Mountains.add(mountain3)
Mountains.add(mountain4)
'''

# Code Archive - Gradient
'''
# = Make Gradient =
gradient = Layer()

gradient1 = Rectangle(400, 400)
gradient1.setFillColor((143,123,163))
gradient1.move(200, 350)
gradient1.setBorderWidth(0)  # No border
gradient.add(gradient1)

gradient2 = Rectangle(400, 400)
gradient2.setFillColor((172,116,155	))
gradient2.move(200, 400)
gradient2.setBorderWidth(0)  # No border
gradient.add(gradient2)

gradient3 = Rectangle(400, 400)
gradient3.setFillColor((188,104,143	))
gradient3.move(200, 450)
gradient3.setBorderWidth(0)  # No border
gradient.add(gradient3)

gradient4 = Rectangle(400, 400)
gradient4.setFillColor((215,94,136))
gradient4.move(200, 500)
gradient4.setBorderWidth(0)  # No border
gradient.add(gradient4)

gradient5 = Rectangle(400, 400)
gradient5.setFillColor((234,83,121))
gradient5.move(200, 550)
gradient5.setBorderWidth(0)  # No border
gradient.add(gradient5)

gradient6 = Rectangle(400, 400)
gradient6.setFillColor(ImageColor.getcolor("#E54A79","RGB"))
gradient6.move(200, 600)
gradient6.setBorderWidth(0)  # No border
gradient.add(gradient6)

gradient7 = Rectangle(400, 400)
gradient7.setFillColor(ImageColor.getcolor("#FEB87B","RGB"))
gradient7.move(200, 550)
gradient7.setBorderWidth(0)  # No border
gradient.add(gradient7)

gradient8 = Rectangle(400, 400)
gradient8.setFillColor(ImageColor.getcolor("#FC713E","RGB"))
gradient8.move(200, 600)
gradient8.setBorderWidth(0)  # No border
gradient.add(gradient8)
'''

'''
# =  1. Animation =  (PERFORMANCE ISSUE)
for i in range(500):
    PoB.move(1, 0)
    # if i % 100 == 0:
    #     Clouds.move(1,0)
    Mountains.move(0.05, 0)
    Sun.move(0.001,0)
    Reflect.move(0.001,0)
    # if i % 50 == 0:
    if i >= 400:
        Trains.move(-(0.001 + (0.01 * j * j)), 0)
        j += 1
        
    if c4 == cnt4:
        comets["comets{0}".format(c4)] = Comet(random.randrange(160, 450),random.randrange(-20, 40),15, 0.27, 0.9)
        cnt4 += 1  # 살별 중복 생성 방지
    if comets["comets{0}".format(c4)].drop(-2, 1) == True:  # 살별 생명 감소 및 삭제
        c4 += 1  # 다음 살별로 넘어가기
    if c9 == cnt9:
        comets1["comets{0}".format(c9)] = Comet(random.randrange(40, 350),random.randrange(20, 130),7, 0.11, 0.9)
        cnt9 += 1  # 살별 중복 생성 방지
    if comets1["comets{0}".format(c9)].drop(-1, 1) == True:  # 살별 생명 감소 및 삭제
        c9 += 1  # 다음 살별로 넘어가기
    sleep(0.05)
    
# Transition
for i in range(500):
    Background.move(0,1)
    Foreground.move(0,2)
    # sleep(0.01) waht? lag
'''