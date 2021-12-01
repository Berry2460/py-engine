import engine

def main():
    x=1280
    y=720
    win=engine.Window(x, y, 'engine', vsync=0, fullscreen=False)
    #load textures
    t1=engine.Texture('textures/dragon.png',4,4)
    t2=engine.Texture('textures/grass.png',1,1)
    t3=engine.Texture('textures/tower.png',1,1)
    #setup camera and map
    cam=engine.Camera(win,0,0,2.0)
    cam.scale=(y/480)*2
    env=engine.Environment(win, t2, 64,64, 64,64, 4) #total size, floor size, collision subdiv amount
    #add floors
    env.place(7, 9, t3, True)
    env.place(14, 10, t3, True)
    env.place(9, 15, t3, True)
    #make sprites
    player=engine.Sprite(win, env, t1, 10, 12, 128, 128)
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
        if cam.scale < (y/480):
            cam.scale=(y/480)
        #exit
        if win.isPressed(ord('A')):
            win.close()
            return
        #walk animation
        if win.timerCheck(0.3):
            win.timerStart()
            player.enumTextureCoords(0,1)
        #follow mouse
        if win.leftMouseButton():
            #movement
            collide=False
            if win.winy/2+(player.ylen/10) < win.getMousePos()[1]:
                player.setTextureCoordX(0)
                collide=player.move(0, 200)
            elif win.winy/2-(player.ylen/10) > win.getMousePos()[1]:
                player.setTextureCoordX(2)
                collide=player.move(0, -200)
            if win.winx/2+(player.xlen/10) < win.getMousePos()[0]:
                player.setTextureCoordX(1)
                collide=player.move(200, 0)
            elif win.winx/2-(player.xlen/10) > win.getMousePos()[0]:
                player.setTextureCoordX(3)
                collide=player.move(-200, 0)
        cam.center(player)

if __name__ == '__main__':
    main()
