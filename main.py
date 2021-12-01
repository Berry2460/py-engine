import engine

def main():
    x=1280
    y=720
    win=engine.Window(x, y, 'engine', vsync=0, fullscreen=False)
    #load textures
    t1=engine.Texture('textures/dragon.png',3,4)
    t2=engine.Texture('textures/grass.png',1,1)
    t3=engine.Texture('textures/tower.png',1,1)
    #setup camera and map
    cam=engine.Camera(win,0,0,2.0)
    cam.scale=(y/480)*2.5
    env=engine.Environment(win, t2, 64,64, 32,32, 4) #total size, floor size, collision subdiv amount
    #add floors
    env.place(8, 7, t3, True)
    env.place(9, 7, t3, True)
    env.place(16, 10, t3, True)
    env.place(9, 15, t3, True)
    #make sprites
    player=engine.Sprite(win, env, t1, 10, 12, 128, 96, solid=True, half=True)
    enemy=engine.Sprite(win, env, t1, 1, 9, 96, 64, solid=True, half=True)
    enemy.setTextureCoordX(1)
    enemy.tint(0.0, 1.0, 1.0) #remove red colors from enemy
    pwalk=engine.Timer() #walk animation timer
    ewalk=engine.Timer() #walk animation timer for enemy
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
            player.enumTextureCoords(0,1)
            #enemy animation
            enemy.enumTextureCoords(0,1)
        #enemy moving
        if ewalk.timerCheck(0.01):
            enemy.move(70, 0)
            ewalk.timerStart()
        #follow mouse
        if win.leftMouseButton():
            #movement
            collide=False
            if win.winy/2+(player.ylen/2) < win.getMousePos()[1]:
                player.unflipTexture()
                player.setTextureCoordX(0)
                collide=player.move(0, 180)
            elif win.winy/2-(player.ylen/2) > win.getMousePos()[1]:
                player.unflipTexture()
                player.setTextureCoordX(2)
                collide=player.move(0, -180)
            if win.winx/2+(player.xlen/2) < win.getMousePos()[0]:
                player.unflipTexture()
                player.setTextureCoordX(1)
                collide=player.move(180, 0)
            elif win.winx/2-(player.xlen/2) > win.getMousePos()[0]:
                player.flipTexture()
                player.setTextureCoordX(1)
                collide=player.move(-180, 0)
            if collide:
                #collision stuff here
                pass
        cam.center(player)

if __name__ == '__main__':
    main()
