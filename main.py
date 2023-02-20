import engine

class Enemy:
    def __init__(self, win, env, tex, x, y):
        self.startx=x
        self.starty=y
        self.enemy=engine.Sprite(win, env, tex, x, y, 64, 48, solid=True, half=True)
        self.enemy.setTextureCoordX(2)
        self.enemy.tint(0.0, 1.0, 1.0)
        self.goRight=True
        self.walk=engine.Timer() #enemy walk animation timer
        self.alive=True
        self.dying=False

    def move(self, player):
        #walk animation
        c=False
        if not self.dying:
            if self.walk.timerCheck(0.3):
                self.walk.timerStart()
                self.enemy.enumTextureCoordY(1, 0, 4)
            #enemy moving
            if self.goRight:
                self.enemy.unflipTexture()
                c=self.enemy.move(100, 0)
            else:
                self.enemy.flipTexture()
                c=self.enemy.move(-100, 0)
            if c:
                if self.enemy.checkCollision() == player:
                    self.enemy.setTextureCoordX(0)
                    self.dying=True
                else:
                    self.goRight=not self.goRight
        else:
            self.die()
            
    def die(self):
        if self.walk.timerCheck(0.16):
            self.walk.timerStart()
            self.enemy.unflipTexture()
            self.enemy.setTextureCoordY(5)
            if self.enemy.enumOnceTextureCoordX(1, 0, 5):
                self.enemy.remove()
                self.alive=False

def walk(walk, sprite):
    #walk animation
    if walk.timerCheck(0.3):
        walk.timerStart()
        sprite.enumTextureCoordY(1, 0, 4)



def controls(win, player):
    #follow mouse
    if win.leftMouseButton():
        #movement
        collide=False
        up=0 #directions
        if win.winy/2+(player.ylen/2) < win.getMousePos()[1]:
            up=1
            player.unflipTexture()
            player.setTextureCoordX(0)
            collide=player.move(0, 180)
        elif win.winy/2-(player.ylen/2) > win.getMousePos()[1]:
            up=-1
            player.unflipTexture()
            player.setTextureCoordX(4)
            collide=player.move(0, -180)
        if win.winx/2+(player.xlen/2) < win.getMousePos()[0]:
            player.unflipTexture()
            if up == 0:
                player.setTextureCoordX(2)
            elif up == 1:
                player.setTextureCoordX(1)
            elif up == -1:
                player.setTextureCoordX(3)
            collide=player.move(180, 0)
        elif win.winx/2-(player.xlen/2) > win.getMousePos()[0]:
            player.flipTexture()
            if up == 0:
                player.setTextureCoordX(2)
            elif up == 1:
                player.setTextureCoordX(1)
            elif up == -1:
                player.setTextureCoordX(3)
            collide=player.move(-180, 0)
        if collide:
            #collision stuff here
            pass
    elif win.rightMouseButton():
        player.setTextureCoordY(4)

def main():
    x=800
    y=600
    win=engine.Window(x, y, 'engine', vsync=0, fullscreen=False)
    #load textures
    t1=engine.Texture('textures/dragon.png',5,6)
    t2=engine.Texture('textures/tileset.png',2,1)
    t3=engine.Texture('textures/font.png',6,6)
    #set font
    win.setFont(t3)
    #setup camera and map
    cam=engine.Camera(win,0,0,2.0)
    cam.scale=(y/480)*2.5
    env=engine.Environment(win, t2, 24,24, 32,32, 4) #total size, floor size, collision subdiv amount
    #add floors
    env.place(8,7, 1,0, True) #map x,y tileset x,y
    env.place(9,7, 1,0, True)
    env.place(16,10, 1,0, True)
    env.place(9,15, 1,0, True)
    #make sprites
    player=engine.Sprite(win, env, t1, 10, 12, 96, 64, solid=True, half=True)
    enemies=[]
    enemies.append(Enemy(win, env, t1, 1, 11))
    enemies.append(Enemy(win, env, t1, 2, 12))
    enemies.append(Enemy(win, env, t1, 1, 9))
    enemies.append(Enemy(win, env, t1, 3, 9))
    enemies.append(Enemy(win, env, t1, 4, 7))
    enemies.append(Enemy(win, env, t1, 3, 5))
    pwalk=engine.Timer() #walk animation timer
    
    #game loop
    helpscreen=True
    showfps=True
    while win.windowLoop():
        #rendering
        win.clear()
        env.render(cam)
        #draw FPS
        if showfps:
            win.setFontSize(16)
            win.renderText('FPS '+str(int(win.getFps())), 0,0)
        #help screen text
        if helpscreen:
            win.setFontSize(30)
            win.renderText('welcome', 0.38,0.3)
            win.setFontSize(20)
            win.renderText('press a to exit', 0.3,0.60)
            win.renderText('press b to respawn dragon', 0.20,0.65)
            win.renderText('press h to toggle helpscreen', 0.17,0.70)
            win.renderText('press f to toggle FPS', 0.23,0.75)
            win.renderText('use left click to move', 0.22,0.80)
        #scroll zoom
        if win.scrollWheel() == 1:
            cam.scale+=0.1
        elif win.scrollWheel() == -1:
            cam.scale-=0.1
        if cam.scale < (y/480)*2:
            cam.scale=(y/480)*2
        #exit
        if win.isPressed(ord('A')):
            win.close()
            return
        #respawn enemy
        elif win.isPressed(ord('B')):
            for i in range(len(enemies)):
                if not enemies[i].alive and not enemies[i].enemy.isVisible():
                    sx=enemies[i].startx
                    sy=enemies[i].starty
                    enemies[i]=Enemy(win, env, t1, sx, sy)
        elif win.isPressed(ord('H')):
            helpscreen=not helpscreen
            win.haltKey(ord('H'))
        elif win.isPressed(ord('F')):
            showfps=not showfps
            win.haltKey(ord('F'))
        #animations
        walk(pwalk, player)
        #enemy logic
        for enemy in enemies:
            if enemy.alive:
                enemy.move(player)
        #do controls
        controls(win, player)
        #center camera on player
        cam.center(player)

if __name__ == '__main__':
    main()
