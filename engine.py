import glfw
import OpenGL.GL as gl
import PIL.Image
import time

##### TIMER #####

class Timer:
    def __init__(self):
        self.timer=0

    def timerStart(self):
        self.timer=time.time()

    def timerCheck(self, t):
        return (time.time()-self.timer >= t)

##### ENVIRONMENT #####

class Environment:
    def __init__(self, window, floor, x=128, y=128, tilex=64, tiley=64, subdiv=4):
        while tilex%subdiv != 0 or tiley%subdiv != 0:
            subdiv+=1 #subdiv must divide evenly into tile size to prevent collision errors
        self.subdiv=subdiv
        self.x=x
        self.y=y
        self.cx=x*self.subdiv
        self.cy=y*self.subdiv
        self.tilex=tilex
        self.tiley=tiley
        self.ctilex=int(tilex/self.subdiv)
        self.ctiley=int(tiley/self.subdiv)
        self.world=[[]]
        self.collision=[[]]
        self.window=window
        #world init
        for i in range(self.y):
            for j in range(self.x):
                self.world[i].append(floor) #texture
            self.world.append([])
        #collision init
        for i in range(self.cy):
            for j in range(self.cx):
                self.collision[i].append([False, False]) #is occupied, sprite
            self.collision.append([])

    def place(self, x, y, texture, solid=False):
        self.world[y][x]=texture
        cx=x*self.subdiv
        cy=(y-1)*self.subdiv
        cendx=(x+1)*self.subdiv
        cendy=y*self.subdiv
        for i in range(cy, cendy):
            for j in range(cx, cendx):
                self.collision[i][j][0]=solid
                self.collision[i][j][1]=solid

    def render(self, camera):
        sprites=[]
        xmin=-int((self.window.winx/self.tilex)/camera.scale)-2
        xmax=int((self.window.winx/self.tilex)/camera.scale)+2
        ymin=-int((self.window.winy/self.tiley)/camera.scale)-1
        ymax=int((self.window.winy/self.tiley)/camera.scale)+3
        for i in reversed(range(ymin, ymax)):
            for j in range(xmin, xmax):
                ty=min(self.y-1, max(0, i+int(camera.y/self.tiley)))
                tx=min(self.x-1, max(0, j+int(camera.x/self.tilex)))
                cty=ty*self.subdiv
                ctx=tx*self.subdiv
                #sprite culling
                for y in range(0, self.subdiv, 2):
                    for x in range(0, self.subdiv, 2):
                        sprite=self.collision[cty+y][ctx+x][1]
                        if type(sprite) == Sprite and sprite not in sprites:
                            sprites.append(sprite)
                #render tiles
                gl.glBindTexture(gl.GL_TEXTURE_2D, self.world[ty][tx].getTexture())
                gl.glBegin(gl.GL_QUADS)
                y=(i*self.tiley)-(camera.y%self.tiley)
                x=(j*self.tilex)-(camera.x%self.tilex)
                gl.glColor3f(1.0, 1.0, 1.0)
                gl.glTexCoord2f(0.0, 0.0)
                gl.glVertex2f(x/self.window.winx*camera.scale, (y)/self.window.winy*camera.scale)
                gl.glTexCoord2f(0.0, 1.0)
                gl.glVertex2f((x+self.tilex)/self.window.winx*camera.scale, (y)/self.window.winy*camera.scale)
                gl.glTexCoord2f(1.0, 1.0)
                gl.glVertex2f((x+self.tilex)/self.window.winx*camera.scale, (y-self.tiley)/self.window.winy*camera.scale)
                gl.glTexCoord2f(1.0, 0.0)
                gl.glVertex2f(x/self.window.winx*camera.scale, (y-self.tiley)/self.window.winy*camera.scale)
                gl.glEnd()
        #render sprites
        while len(sprites) > 0:
            for sprite in sprites:
                depth=0
                for sprite2 in sprites:
                    if sprite2 != sprite and sprite.y >= sprite2.y:
                        depth+=1
                if depth == len(sprites)-1:
                    sprite.render(camera)
                    sprites.remove(sprite)

##### TEXTURE #####

class Texture:
    MAX=256
    texCount=0
    textures=[0]*MAX

    def __init__(self, path, x=1, y=1):
        self.data=Texture.texCount
        self.xmax=x
        self.ymax=y
        self.imgX=1
        self.imgY=1
        if Texture.texCount < Texture.MAX:
            img=PIL.Image.open(path).convert('RGBA')
            self.imgX, self.imgY=img.size
            data=img.load()
            pixels=[0]*self.imgX*self.imgY*4
            index=0
            for i in range(self.imgX):
                for j in range(self.imgY):
                    pixels[index]=data[i,j][0]
                    pixels[index+1]=data[i,j][1]
                    pixels[index+2]=data[i,j][2]
                    pixels[index+3]=data[i,j][3]
                    index+=4
            gl.glBindTexture(gl.GL_TEXTURE_2D, Texture.texCount);
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
            gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.imgX, self.imgY, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pixels);
            Texture.texCount+=1

    def getTexture(self):
        return self.data

    def getSizeX(self):
        return self.imgX

    def getSizeY(self):
        return self.imgY

##### CAMERA #####

class Camera:
    def __init__(self, window, x=0, y=0, scale=1.0):
        self.x=x
        self.y=y
        self.scale=scale
        self.window=window

    def move(self, x, y):
        self.x+=x/self.window.getFps()
        self.y+=y/self.window.getFps()

    def center(self, sprite):
        self.x=sprite.x+(sprite.xlen/2)
        self.y=sprite.y-(sprite.ylen/2)

##### SPRITE #####

class Sprite:
    def __init__(self, window, env, texture, x=0, y=0, xlen=32, ylen=32, solid=True, half=False):
        self.half=half
        self.x=x*env.tilex
        self.y=y*env.tiley
        self.tx=0
        self.ty=0
        self.xlen=xlen
        self.ylen=ylen
        self.color=[1.0, 1.0, 1.0]
        self.window=window
        self.texture=texture
        self.env=env
        self.solid=solid
        self.visible=True
        self.setCollision(True)
        self.flip=False

    def tint(self, r, g, b):
        self.color[0]=r
        self.color[1]=g
        self.color[2]=b

    def flipTexture(self):
        self.flip=True

    def unflipTexture(self):
        self.flip=False

    def remove(self):
        self.visible=False
        self.setCollision(False)

    def isVisible(self):
        return self.visible

    def render(self, camera):
        if self.visible:
            minTextureX=self.tx/self.texture.xmax
            minTextureY=self.ty/self.texture.ymax
            maxTextureX=(self.tx+1)/self.texture.xmax
            maxTextureY=(self.ty+1)/self.texture.ymax
            if self.flip:
                temp=minTextureX
                minTextureX=maxTextureX
                maxTextureX=temp
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture.getTexture())
            gl.glBegin(gl.GL_QUADS)
            gl.glColor3f(self.color[0], self.color[1], self.color[2])
            gl.glTexCoord3f(minTextureY, minTextureX, self.y/(self.env.y*self.env.tiley))
            gl.glVertex2f((self.x-camera.x)/self.window.winx*camera.scale, (self.y-camera.y)/self.window.winy*camera.scale)
            gl.glTexCoord3f(minTextureY, maxTextureX, self.y/(self.env.y*self.env.tiley))
            gl.glVertex2f((self.x-camera.x+self.xlen)/self.window.winx*camera.scale, (self.y-camera.y)/self.window.winy*camera.scale)
            gl.glTexCoord3f(maxTextureY, maxTextureX, self.y/(self.env.y*self.env.tiley))
            gl.glVertex2f((self.x-camera.x+self.xlen)/self.window.winx*camera.scale, (self.y-camera.y-self.ylen)/self.window.winy*camera.scale)
            gl.glTexCoord3f(maxTextureY, minTextureX, self.y/(self.env.y*self.env.tiley))
            gl.glVertex2f((self.x-camera.x)/self.window.winx*camera.scale, (self.y-camera.y-self.ylen)/self.window.winy*camera.scale)
            gl.glEnd()

    def move(self, x, y):
        oldx=self.x
        oldy=self.y
        self.setCollision(False)
        self.x+=x/self.window.getFps()
        self.y+=y/self.window.getFps()
        hit=self.getCollision()
        #collision detection
        if hit or self.x < 0 or self.y < self.ylen/2 or self.x > self.env.x*self.env.tilex-self.xlen/2 or self.y > self.env.y*self.env.tiley:
            self.x=oldx
            self.y=oldy
            if not hit:
                hit=True
        self.setCollision(True)
        return hit

    def setCollision(self, value):
        off=0
        if self.half:
            off=int(self.ylen/2)
        y=int((self.y-off)/self.env.ctiley)
        x=int(self.x/self.env.ctilex)
        y2=int((self.y-self.ylen)/self.env.ctiley)
        x2=int((self.x+self.xlen)/self.env.ctilex)
        for i in range(max(0, y2), min(y+1, self.env.cy)):
            for j in range(max(0, x), min(x2+1, self.env.cx)):
                if self.solid:
                    self.env.collision[i][j][0]=value
                if value and (self.env.collision[i][j][1] == False or self.env.collision[i][j][1] == self):
                    self.env.collision[i][j][1]=self
                elif not value and self.env.collision[i][j][1] == self:
                    self.env.collision[i][j][1]=False

    def getCollision(self):
        if self.solid:
            off=0
            if self.half:
                off=int(self.ylen/2)
            y=int((self.y-off)/self.env.ctiley)
            x=int(self.x/self.env.ctilex)
            y2=int((self.y-self.ylen)/self.env.ctiley)
            x2=int((self.x+self.xlen)/self.env.ctilex)
            for i in range(max(0, y2), min(y+1, self.env.cy)):
                for j in range(max(0, x), min(x2+1, self.env.cx)):
                    if self.env.collision[i][j][0]:
                        return self.env.collision[i][j][1]
        return False

    def setTextureCoordX(self, x=0):
        self.tx=x

    def setTextureCoordY(self, y=0):
        self.ty=y

    def enumTextureCoordX(self, x=0, wrapMin=0, wrapMax=0):
        self.tx=(self.tx+x)%min(wrapMax, self.texture.xmax)+wrapMin

    def enumTextureCoordY(self, y=0, wrapMin=0, wrapMax=0):
        self.ty=(self.ty+y)%min(wrapMax, self.texture.ymax)+wrapMin

    def enumOnceTextureCoordX(self, x=0, wrapMin=0, wrapMax=0):
        step=self.tx+x
        mod=min(wrapMax, self.texture.xmax)
        out=False
        if step >= mod:
            out=True
        self.tx=step%mod+wrapMin
        return out

    def enumOnceTextureCoordY(self, y=0, wrapMin=0, wrapMax=0):
        step=self.ty+y
        mod=min(wrapMax, self.texture.ymax)
        out=False
        if step >= mod:
            out=True
        self.ty=step%mod+wrapMin
        return out

##### WINDOW #####

class Window:
    def __init__(self, x=640, y=480, name='Engine', fullscreen=False, vsync=1):
        if not glfw.init():
            return
        if (fullscreen):
            self.window=glfw.create_window(x, y, name, glfw.get_primary_monitor(), None)
        else:
            self.window=glfw.create_window(x, y, name, None, None)
        if not self.window:
            glfw.terminate()
            return
        #window context
        glfw.make_context_current(self.window)
        glfw.swap_interval(vsync)
        glfw.set_key_callback(self.window, self._buttons)
        glfw.set_cursor_pos_callback(self.window, self._mousepos)
        glfw.set_mouse_button_callback(self.window, self._mouse)
        glfw.set_scroll_callback(self.window, self._scroll)
        #gl context
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        #vars
        self.mouse=[0,0] #mouse position
        self.keys=[False]*512 #keys
        self.mclick=[False]*3 #mouse buttons
        self.fps=0
        self.frames=60 #start above 0 to prevent miscalculations due to inaccuracy
        self.start=time.time()
        self.winx=x
        self.winy=y
        self.scroll=0
        #texture initialization
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glGenTextures(Texture.MAX, Texture.textures)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def windowLoop(self):
        self.scroll=0
        if not glfw.window_should_close(self.window):
            self.frames+=1
            if time.time()-self.start > 0:
                self.fps=self.frames/(time.time()-self.start)
            if time.time()-self.start >= 1:
                self.start=time.time()
                self.frames=0
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            return True
        else:
            glfw.terminate()
            return False

    def _buttons(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key]=True
        elif action == glfw.RELEASE:
            self.keys[key]=False

    def _mousepos(self, window, x, y):
        self.mouse[0]=x
        self.mouse[1]=self.winy-y

    def _mouse(self, window, key, action, mods):
        if action == glfw.PRESS:
            self.mclick[key]=True
        elif action == glfw.RELEASE:
            self.mclick[key]=False

    def _scroll(self, window, xoff, yoff):
        if yoff > 0:
            self.scroll=1
        elif yoff < 0:
            self.scroll=-1

    def close(self):
        glfw.destroy_window(self.window)

    def scrollWheel(self):
        return self.scroll
        
    def isPressed(self, key):
        return self.keys[key]
    
    def getMousePos(self):
        return self.mouse
    
    def leftMouseButton(self):
        return self.mclick[0]
    
    def rightMouseButton(self):
        return self.mclick[1]
    
    def middleMouseButton(self):
        return self.mclick[2]
    
    def getFps(self):
        return self.fps

    def setTitle(self, title):
        glfw.set_window_title(self.window, title)

    def resize(self, x, y):
        self.winx=x
        self.winy=y
        glfw.set_window_size(self.window, x, y)

    def clear(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(0.2, 0.2, 0.2, 1.0)

    def vsync(self, vsync):
        glfw.swap_interval(vsync)
