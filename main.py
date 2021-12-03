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
    x=800
    y=600
    win=engine.Window(x, y, 'engine', vsync=0, fullscreen=False)
    #load textures
    t1=engine.Texture('textures/dragon.png',5,6)
    t2=engine.Texture('textures/tileset.png',2,2)
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
    enemy=spawnEnemy(win, env, t1)
    enemyRight=[True] #enemy move right
    enemyAlive=True
    pwalk=engine.Timer() #walk animation timer
    ewalk=engine.Timer() #enemy walk animation timer
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
            if not enemyAlive and not enemy.isVisible():
                enemy=spawnEnemy(win, env, t1)
                enemyAlive=True
                enemyRight=[True]
        elif win.isPressed(ord('H')):
            helpscreen=not helpscreen
            win.haltKey(ord('H'))
        elif win.isPressed(ord('F')):
            showfps=not showfps
            win.haltKey(ord('F'))
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
