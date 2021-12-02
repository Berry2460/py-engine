import engine

def main():
    x=1280
    y=720
    win=engine.Window(x, y, 'engine', vsync=0, fullscreen=False)
    #load textures
    t1=engine.Texture('textures/dragon.png',5,6)
    t2=engine.Texture('textures/grass.png',1,1)
    t3=engine.Texture('textures/tower.png',1,1)
    #setup camera and map
    cam=engine.Camera(win,0,0,2.0)
    cam.scale=(y/480)*2.5
    env=engine.Environment(win, t2, 24,24, 32,32, 4) #total size, floor size, collision subdiv amount
    #add floors
    env.place(8, 7, t3, True)
    env.place(9, 7, t3, True)
    env.place(16, 10, t3, True)
    env.place(9, 15, t3, True)
    #make sprites
    player=engine.Sprite(win, env, t1, 10, 12, 96, 64, solid=True, half=True)
    enemy=engine.Sprite(win, env, t1, 1, 9, 64, 48, solid=True, half=True)
    enemy.setTextureCoordX(2)
    enemyRight=True #enemy move right
    enemy.tint(0.0, 1.0, 1.0) #remove red colors from enemy
    pwalk=engine.Timer() #walk animation timer
    #game loop
    while win.windowLoop():
        #rendering
        win.setTitle('engine FPS: '+str(int(win.getFps())))
        win.clear()
        env.render(cam)
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
        #walk animation
        if pwalk.timerCheck(0.3):
            pwalk.timerStart()
            player.enumTextureCoordY(1, 0, 3)
            #enemy animation
            enemy.enumTextureCoordY(1, 0, 3)
        #enemy moving
        c=False
        if enemyRight:
            enemy.unflipTexture()
            c=enemy.move(100, 0)
        else:
            enemy.flipTexture()
            c=enemy.move(-100, 0)
        if c:
            enemyRight=not enemyRight
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
        cam.center(player)

if __name__ == '__main__':
    main()
