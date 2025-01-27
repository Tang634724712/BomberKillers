import pygame as pg
import time as shijian
import random
import sys
from os import path
from settings import *
from object import *
import socket
import threading as xianchen
class Game:
    def __init__(self):
        # initalize game window, etc...
        pg.init()
        '''
        pg.mixer.init()
        self.music=pg.mixer.music.load("image/1.mp3")
        self.music=pg.mixer.music.load("image/2.mp3")
        '''
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # Let the key press down
        pg.key.set_repeat(500, 100)
        #main interface
        self.mian_jiemian=pg.image.load("image/mainground.png")
        self.chuangjian_fj1=pg.image.load("BNB/xz1.png")
        self.chuangjian_fj2=pg.image.load("BNB/xz2.png")
        self.room=pg.image.load("BNB/room.png")
        self.black=pg.image.load("BNB/black.png")
        #
        #
        self.sever=None
        self.client=None
        self.msg=""
        self.lianjie=False
        self.box_msg=""
        self.change_xinxi=False
        
        self.thread=None
        self.player_msg_list=[]
        
        self.player_play_list=[]
       
        self.play_imformation_list=[]
        self.play_imformation_kuang=pg.image.load("image/play_imformation/play information box.png")
        
        self.bomb_sjb="2|"
        self.daoju_sjb = "5|"  
        self.robot_sjb = "3|"  
        self.robot_bomb_sjb = "4|"  
        self.box_sjb = "7|"  
        #
        self.zhen=255
        self.wall_list=[]
        self.daoju_list=[]
        self.robot_list=[]
        self.robot_bomb=[]
        self.box_list=[]
        self.load_data()
        self.running = True
        self.bomb=[]
        self.cunfang=""
        self.bomb_shuliang=0
        self.jiemian=0
        
        self.player_index=0
        self.name=""
        self.x=0
        self.jishu=0
        self.choice_name()
        #32x24
        #pg.mixer.music.play(-1)
       
    def choice_name(self):
        self.name=random.choice(["Clever ","Naughty ","Handsome "," violent ","rich ","low-key ","steady ","Jovial"])+random.choice(["Duck","pig","froggy","John Doe","Passerby B","Bystander C","Xiao Ming","Xiao Hong","Xiao Zhang","Xiao Pao"])
    def receive(self):
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((socket.gethostbyname(socket.gethostname()), 2001))
            self.server.listen(5)
            self.client, ip = self.server.accept()
            self.lianjie=True
            while True:
                try:
                    msg = self.client.recv(1024).decode("utf-8")

                    if msg.split("|")[0] == "1":
                        print(msg)
                        self.player_play1.x = int(msg.split("|")[1].split(",")[0])
                        self.player_play1.y = int(msg.split("|")[1].split(",")[1])
                    elif msg.split("|")[0] == "2":
                    
                        if len(msg.split("|")[1].split("*"))-1!=self.robot_bomb:
                            self.map_data[int(msg.split("|")[1].split(",")[1])] = self.map_data[int(msg.split("|")[1].split(",")[1])][:int(msg.split("|")[1].split(",")[0])] + "3" + self.map_data[int(msg.split("|")[1].split(",")[1])][int(msg.split("|")[1].split(",")[0]) + 1:]
                            self.bomb.append(Bomb(int(msg.split("|")[1].split(",")[0]), int(msg.split("|")[1].split(",")[1]), self.screen, self.map_data, int(msg.split("|")[1].split(",")[2]), "123"))
                    elif msg.split("|")[0]== "3":
                        for i in range(0,len(msg.split("|")[1].split("."))):
                            self.robot_list[i].x=int(msg.split("|")[1].split(".")[i].split(",")[0])
                            self.robot_list[i].y=int(msg.split("|")[1].split(".")[i].split(",")[1])
                    elif msg.split("|")[0]=="4":
                        self.map_data[int(msg.split("|")[1].split(",")[1])] = self.map_data[int(msg.split("|")[1].split(",")[1])][:int(msg.split("|")[1].split(",")[0])] + "3" + self.map_data[int(msg.split("|")[1].split(",")[1])][int(msg.split("|")[1].split(",")[0]) + 1:]
                        self.robot_bomb.append(Bomb(int(msg.split("|")[1].split(",")[0]), int(msg.split("|")[1].split(",")[1]), self.screen, self.map_data, int(msg.split("|")[1].split(",")[2]), "guaishou"))
                        print("ok")
                    elif msg.split("|")[0]=="5":
                        self.daoju_list.append(Daoju(self.screen,int(msg.split("|")[1].split(",")[0]),int(msg.split("|")[1].split(",")[1]),int(msg.split("|")[1].split(",")[2])))
                    elif msg.split("|")[0]=="6":
                        del self.daoju_list[int(msg.split("|")[1])]
                    elif msg.split("|")[0]=="7":
                        del self.box_list[int(msg.split("|")[1])]
                except:
                    pass
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("192.168.0.178", 5000))
        self.client.sendall((("1|init|"+str(2)+","+self.name+",no ready")+".").encode("utf8"))
        while True:
            try:
                msg = self.client.recv(1024).decode("utf-8")
                print(msg)
                if msg.split("|")[0] == "1":
                    if msg.split("|")[1]=="Enter game":
                        self.jiemian=4
                    if msg.split("|")[1]=="msg":
                        self.change_xinxi=True
                        self.player_msg_list = []
                        for i in range(0, len(msg.split("|")[2].split(".")) - 1):
                            if msg.split("|")[2].split(".")[i] != "-1,no name,no ready":
                                self.player_msg_list.append(player_icons(self.screen, int(msg.split("|")[2].split(".")[i].split(",")[0]),msg.split("|")[2].split(".")[i].split(",")[1], i,msg.split("|")[2].split(".")[i].split(",")[2]))
                        self.change_xinxi=False
                elif msg.split("|")[0] == "2":
                    
                    if msg.split("|")[1] == "js":
                        print(msg)
                        
                        if self.player_index==0:
                            for i in range(0,len(msg.split("|")[2].split(".")) - 1):
                                if msg.split("|")[2].split(".")[i].split(",")[4] == self.name:self.player_index = i
                                self.player_play_list.append(Player(int(msg.split("|")[2].split(".")[i].split(",")[0]),int(msg.split("|")[2].split(".")[i].split(",")[1]),self.screen,int(msg.split("|")[2].split(".")[i].split(",")[2])))
                                self.play_imformation_list.append(Play_imformation(self.screen,int(msg.split("|")[2].split(".")[i].split(",")[2]),msg.split("|")[2].split(".")[i].split(",")[4],int(msg.split("|")[2].split(".")[i].split(",")[5])))
                        else:
                            for i in range(0,len(msg.split("|")[2].split(".")) - 1):
                                if msg.split("|")[2].split(".")[i] == "None":
                                    if self.player_play_list[i] != None:
                                        print("ok")
                                        self.player_play_list[i] = None
                                        self.play_imformation_list[i] = None
                    elif msg.split("|")[1] == "end":
                        self.end_kuang=end_kuang(self.screen,self.play_imformation_list,int(msg.split("|")[2]),self.player_index)
                        self.shu_ying=True
                    elif msg.split("|")[1] == "chat":
                        self.chat_box.add_information(msg.split("|")[2])
                    elif msg.split("|")[1] == "property":
                        zhen=0
                        index=0
                        add=False
                        while True:
                            if index==len(self.daoju_list):
                                add=True
                                break
                            if index==len(msg.split("|")[2].split("."))-1:
                                i=0
                                while i<len(self.daoju_list):
                                    if self.daoju_list[i].index>=self.daoju_list[index].index:
                                        del self.daoju_list[i]
                                        i-=1
                                    i+=1
                            if self.daoju_list[index].index!=int(msg.split("|")[2].split(".")[index].split(",")[3]):
                                del self.daoju_list[index]
                            else:
                                index+=1
                                zhen+=1
                        if add:
                            for i in range(index,len(msg.split("|")[2].split("."))):
                                self.daoju_list.append(Daoju(self.screen,int(msg.split("|")[2].split(".")[i].split(",")[0]),int(msg.split("|")[2].split(".")[i].split(",")[1]),int(msg.split("|")[2].split(".")[i].split(",")[2]),int(msg.split("|")[2].split(".")[i].split(",")[3])))
                    elif msg.split("|")[1] == "life":
                        for index in range(0,len(msg.split("|")[2].split("."))-1):
                            if len(msg.split("|")[2].split("."))!="None":
                                if int(msg.split("|")[2].split(".")[index]) != self.player_play_list[index].die:
                                    self.player_play_list[index].die = int(msg.split("|")[2].split(".")[index])
                                    self.play_imformation_list[index].zhuang_tai=int(msg.split("|")[2].split(".")[index])
                    elif msg.split("|")[1] == "move":
                        for i in range(0,len(msg.split("|")[2].split(".")) - 1):
                            if msg.split("|")[2].split(".")[i]!="None":
                                self.player_play_list[i].x = int(msg.split("|")[2].split(".")[i].split(",")[0])
                                self.player_play_list[i].y = int(msg.split("|")[2].split(".")[i].split(",")[1])
                    elif msg.split("|")[1]=="box_xinxi":
                        for i in range(0,len(msg.split("|")[2].split(".")) - 1):
                            self.box_list[int(msg.split("|")[2].split(".")[i])].die=1
                    elif msg.split("|")[1] == "box":
                        for i in range(0,len(msg.split("|")[2].split("."))-1):
                            if self.box_list[i]!="No" and msg.split("|")[2].split(".")[i]=="No":
                                self.map_data[self.box_list[i].y]=self.map_data[self.box_list[i].y][:self.box_list[i].x]+"."+self.map_data[self.box_list[i].y][self.box_list[i].x+1:]
                                self.box_list[i]="No"
                    elif msg.split("|")[1]=="bomb":
                        
                        msg_index = 0
                        zhen = 0
                        if msg.split("|")[2]=="":
                            self.bomb=[]
                        else:
                            while True:
                                if zhen+1>len(self.bomb):
                                    break
                                if self.bomb[zhen].index!=int(msg.split("|")[2].split(".")[msg_index].split(",")[0]):
                                    del self.bomb[zhen]
                                    msg_index-=1
                                else:
                                    zhen+=1
                                    msg_index+=1
                            
                            for i in range(zhen,len(msg.split("|")[2].split("."))-1):
                                self.bomb.append(Bomb(int(msg.split("|")[2].split(".")[i].split(",")[1]),
                                                      int(msg.split("|")[2].split(".")[i].split(",")[2]),
                                                      self.screen,
                                                      self.map_data,int(msg.split("|")[2].split(".")[i].split(",")[3]),
                                                      "paopao",
                                                      int(msg.split("|")[2].split(".")[i].split(",")[0])))
            except:
                pass
    def clear(self):
        self.wall_list=[]
        self.daoju_list=[]
        self.robot_list=[]
        self.robot_bomb=[]
        self.box_list=[]
        self.bomb=[]
        self.play_imformation_list=[]
        self.player_play_list=[]
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'image')
        self.background_img = pg.image.load("image/background1.png").convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map/map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line[:-1])
    def new(self):
        xuhao=0
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.wall_list.append(Wall(self.screen, col, row,"wall"))
                elif tile == "a":
                    self.box_list.append(Box(self.screen, col, row,xuhao,"box"))
                    xuhao+=1
    def main_jiemian(self):
        #self.music=pg.mixer.music.load("image/1.mp3")
        #pg.mixer.music.play(-1)
        self.screen = pg.display.set_mode((800, 600))
        self.jiemian=0
        self.zhen=280
        while True:
                if self.zhen>=0:
                    self.zhen-=0.5
                    self.black.set_alpha(self.zhen)
                    self.screen.blit(self.mian_jiemian, (0, 0))
                    self.screen.blit(self.black,(0,0))
                else:
                    self.screen.blit(self.mian_jiemian, (0, 0))
                    self.screen.blit(self.black,(0,0))
                    mousex, mousey = pg.mouse.get_pos()
                    for event in pg.event.get():
                        # check for closing the window
                        if event.type == pg.QUIT:
                            quit()
                        if event.type == pg.MOUSEBUTTONDOWN:
                            # 74 366 342 444
                            # 74 750 342 552
                            if 74 <= mousex <= 342 and 366 <= mousey <= 444:
                                self.jiemian = 1
                                break
                            elif 74 <= mousex <= 342 and 474 <= mousey <= 553:
                                self.jiemian = 2
                                break
                    if self.jiemian!=0:break
                pg.display.update()
    def game_room(self):
        pg.display.set_caption(self.name)
        self.screen = pg.display.set_mode((1202, 900))
        self.jiemian=-1
        if self.thread == None:
            self.thread=xianchen.Thread(target=self.connect, args=())
            
            self.thread.setDaemon(True)
            self.thread.start()
        self.clear()
        ready="no ready"
        self.zhen=280
        while True:
            if self.zhen >= 0:
                self.zhen -= 3
                self.black.set_alpha(self.zhen)
                self.screen.blit(self.room, (0, 0))
                if len(self.player_msg_list)>0:
                    for i in self.player_msg_list:
                        i.update()
                self.screen.blit(self.black, (0, 0))
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit()
            else:
                self.screen.blit(self.room, (0, 0))
                if not self.change_xinxi:
                    if len(self.player_msg_list)>0:
                        for i in self.player_msg_list:
                            i.update()
                mousex, mousey = pg.mouse.get_pos()
                for event in pg.event.get():
                    # check for closing the window
                    if event.type == pg.QUIT:
                        quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if 773 <= mousex <= 1057 and 467 <= mousey <= 824:
                            if ready=="ready":
                                ready="no ready"
                            else:
                                ready="ready"
                            self.client.sendall((("1|msg|2"+","+self.name+","+ready)+".").encode("utf8"))
                if self.jiemian != -1: break
            self.clock.tick(FPS)
            pg.display.update()
    def create_room(self):
        self.screen = pg.display.set_mode((800, 600))
        xuanze=0
        self.jiemian=-1
        while True:
            self.screen.blit(self.mian_jiemian, (0, 0))
            if xuanze==0:
                self.screen.blit(self.chuangjian_fj1,(130,63))
            else:
                self.screen.blit(self.chuangjian_fj2,(131,63))
            mousex, mousey = pg.mouse.get_pos()
            for event in pg.event.get():
                # check for closing the window
                if event.type == pg.QUIT:
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # 130  63   762 478
                    if 165 <= mousex <=288 and 135 <= mousey <=304:
                        xuanze=1
                    elif xuanze==1 and 320 <= mousex <=427 and 424 <= mousey <=461:
                        self.jiemian=3
                        break
                    elif 433 <= mousex <=538 and 424 <= mousey <=461:
                        self.jiemian=0
                        break
                    # 130  63   762 478
            if self.jiemian!=-1:break
            pg.display.update()
    def duoren(self):
        
        self.load_data()
        self.screen = pg.display.set_mode((1280, 768))
        self.chat_box=chat_box(self.screen,self,self.client,"client")
        self.new()
        self.shu_ying=False
        self.end_kuang=None
        self.end_time = 350
        self.zhen = 280
        while True:
            if not self.shu_ying:
                if self.zhen >= 0:
                    self.zhen -= 3
                    self.black.set_alpha(self.zhen)
                    self.draw()
                    self.update()
                    self.screen.blit(self.black, (0, 0))
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            quit()
                else:
                    self.events()
                    self.update()
                    self.draw()
            else:
                self.draw()
                self.update()
                self.end_kuang.update()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit()
                if self.end_time>=0:
                    self.end_time-=1
                else:
                    if self.zhen>=280:
                        self.jiemian=3
                        self.player_index=0
                        break
                    self.zhen+=2.5
                    self.black.set_alpha(self.zhen)
                    self.screen.blit(self.black, (0, 0))
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        quit()
            self.clock.tick(FPS)
            pg.display.update()
    def danren(self):
        for i in range(0,10):
            self.robot_list.append(Robot(self.screen,self.map_data,1))

        #self.music=pg.mixer.music.load("image/2.mp3")
        #pg.mixer.music.play(-1)
        self.screen = pg.display.set_mode((1024, 768))
        while True:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            pg.display.update()
    def run(self):

        # Game loop
        while True:
            if self.jiemian==0:
                self.main_jiemian()
            elif self.jiemian==1:
                self.danren()
            elif self.jiemian==2:
                self.create_room()
            elif self.jiemian==3:
                self.game_room()
            elif self.jiemian==4:
                self.duoren()
    def update(self):
        pass
    def events(self):
        for event in pg.event.get():
        # check for closing the window
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                move=False
                self.chat_box.event(event.key)
                print(event.key)
                if not self.chat_box.useing:
                    if self.player_play_list[self.player_index].die == 0:
                        if event.key==pg.K_SPACE:
                            shifang=False
                            if len(self.bomb)>0:
                                for i in self.bomb:
                                    if i.x==self.player_play_list[self.player_index].x and i.y==self.player_play_list[self.player_index].y:
                                        shifang=True
                            # connect other player       index                             x                                      y                                fanwei
                            if not shifang:
                                self.client.sendall(("2|bomb|"+str(self.player_play_list[self.player_index].x)+","+str(self.player_play_list[self.player_index].y)+","+str(self.player_play_list[self.player_index].fanwei)).encode("utf8"))
                            # self.client.sendall(("2|move|" + str(self.player_index) + "," + str(self.player_play_list[self.player_index].x) + "," + str(self.player_play_list[self.player_index].y) + ".").encode("utf8"))
                        elif event.key == pg.K_LEFT:
                            if len(self.bomb)>0:
                                for i in self.bomb:
                                    if i.x == self.player_play_list[self.player_index].x-1 and i.y == self.player_play_list[self.player_index].y:
                                        move=True
                            if not move and self.map_data[self.player_play_list[self.player_index].y][self.player_play_list[self.player_index].x-1]=="." or self.map_data[self.player_play_list[self.player_index].y][self.player_play_list[self.player_index].x-1]=="3":
                                self.client.sendall(("2|move|" + str(self.player_index) + "," + str(self.player_play_list[self.player_index].x-1) + "," + str(self.player_play_list[self.player_index].y) + ".").encode("utf8"))
                        elif event.key == pg.K_RIGHT:
                            if len(self.bomb) > 0:
                                for i in self.bomb:
                                    if i.x == self.player_play_list[self.player_index].x + 1 and i.y == self.player_play_list[self.player_index].y:
                                        move = True
                            if not move and self.map_data[self.player_play_list[self.player_index].y][self.player_play_list[self.player_index].x+1]=="." or self.map_data[self.player_play_list[self.player_index].y][self.player_play_list[self.player_index].x+1]=="3":
                                self.client.sendall(("2|move|" + str(self.player_index) + "," + str(self.player_play_list[self.player_index].x+1) + "," + str(self.player_play_list[self.player_index].y) + ".").encode("utf8"))
                        elif event.key == pg.K_UP:
                            if len(self.bomb) > 0:
                                for i in self.bomb:
                                    if i.x == self.player_play_list[self.player_index].x and i.y == self.player_play_list[self.player_index].y-1:
                                        move = True
                            if not move and self.map_data[self.player_play_list[self.player_index].y-1][self.player_play_list[self.player_index].x]=="." or self.map_data[self.player_play_list[self.player_index].y-1][self.player_play_list[self.player_index].x]=="3":
                                self.client.sendall(("2|move|" + str(self.player_index) + "," + str(self.player_play_list[self.player_index].x) + "," + str(self.player_play_list[self.player_index].y-1) + ".").encode("utf8"))
                        elif event.key == pg.K_DOWN:
                            if len(self.bomb) >0:
                                for i in self.bomb:
                                    if i.x == self.player_play_list[self.player_index].x and i.y == self.player_play_list[self.player_index].y+1:
                                        move = True
                            if not move and self.map_data[self.player_play_list[self.player_index].y+1][self.player_play_list[self.player_index].x]=="." or self.map_data[self.player_play_list[self.player_index].y+1][self.player_play_list[self.player_index].x]=="3":
                                self.client.sendall(("2|move|" + str(self.player_index) + "," + str(self.player_play_list[self.player_index].x) + "," + str(self.player_play_list[self.player_index].y+1) + ".").encode("utf8"))
              
                #self.client.sendall(("2|move|"+str(self.player_index)+","+str(self.player_play_list[self.player_index].x)+","+str(self.player_play_list[self.player_index].y)+".").encode("utf8"))
    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY,(0,y),(WIDTH,y))

    def draw(self):
        # Game loop - draw
        # Draw / render
        # self.screen.fill(DARKGREY)
        self.screen.blit(self.background_img, [0, 0])
        for i in self.wall_list:
            i.update()
        self.screen.blit(self.play_imformation_kuang,(1024,0))
        for i in self.play_imformation_list:
            if i!=None:
                i.update()
       
        if len(self.daoju_list)>0:
            for i in self.daoju_list:
                i.update()
        if len(self.box_list)>0:
            for index,i in enumerate(self.box_list):
                if i!="No":
                    i.update()
        if len(self.bomb) > 0:#玩家炸弹
            for i in self.bomb:
                i.update()
                if i.time == 0:
                    for x, y in i.list():
                        self.map_data[y] = self.map_data[y][:x] + "." + self.map_data[y][x + 1:]
        for i in self.player_play_list:
            if i!=None:
                i.update()
        # * after drawing everything , flip the display
        
        self.chat_box.update()
    def wait_room(self):
        #room................
        pass
    def show_start_screen(self):
        # Game start screen
        pass
    def show_go_screen(self):
        # Game over screen
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.run()
    g.show_go_screen()

pg.quit()


