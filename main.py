import engine

def spawnEnemy(win, env, tex):
    enemy=engine.Sprite(win, env, tex, 1, 9, 64, 48, solid=True, half=True)
    enemy.setTextureCoordX(2)
    enemy.tint(0.0, 1.0, 1.0)
    return enemy

def moveAI(ai, player, goRight):
    #enemy moving
    c=False
    if goRight[0]:
        ai.unflipTexture()
        c=ai.move(100, 0)
    else:
        ai.flipTexture()
        c=ai.move(-100, 0)
    if c == player:
        return False
    elif c:
        goRight[0]=not goRight[0]
    return True

def walk(walk, sprite):
    #walk animation
    if walk.timerCheck(0.3):
        walk.timerStart()
        sprite.enumTextureCoordY(1, 0, 4)

def die(walk, sprite):
    if walk.timerCheck(0.16):
        walk.timerStart()
        sprite.unflipTexture()
        sprite.setTextureCoordY(5)
        if sprite.enumOnceTextureCoordX(1, 0, 5):
            sprite.remove()

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
    x=1920
    y=1080
    win=engine.Window(x, y, 'engine', vsync=1, fullscreen=True)
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
    enemy=spawnEnemy(win, env, t1)
    enemyRight=[True] #enemy move right
    enemyAlive=True
    pwalk=engine.Timer() #walk animation timer
    ewalk=engine.Timer() #enemy walk animation timer
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
        #respawn enemy
        elif win.isPressed(ord('B')):
            if not enemyAlive and not enemy.isVisible():
                enemy=spawnEnemy(win, env, t1)
                enemyAlive=True
                enemyRight=[True]
        #animations
        walk(pwalk, player)
        #enemy death check
        if enemyAlive:
            walk(ewalk, enemy)
            enemyAlive=moveAI(enemy, player, enemyRight)
            #if died this frame
            if not enemyAlive:
                ewalk.timerStart()
                enemy.unflipTexture()
                enemy.setTextureCoordX(0)
                enemy.setTextureCoordY(5)
        if not enemyAlive and enemy.isVisible():
            die(ewalk, enemy)
        #do controls
        controls(win, player)
        #center camera on player
        cam.center(player)

if __name__ == '__main__':
    main()
