import glm
import glfw
import math
import numpy as np


# Variáveis de janela 
altura = 0
largura = 0
window = 0

# Variaveis de câmera
cameraPos   = glm.vec3(0.0,  0.0,  1.0);
cameraFront = glm.vec3(0.0,  0.0, -1.0);
cameraUp    = glm.vec3(0.0,  1.0,  0.0);

# Modo poligonal
polygonal_mode = False

# Variáveis de mouse
firstMouse = True
yaw = -90.0 
pitch = 0.0
lastX =  largura/2
lastY =  altura/2

# Inputs
tx = 0
ty = 0
tz = 0



def view():
    global cameraPos, cameraFront, cameraUp
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

def projection():
    global altura, largura
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(45.0), largura/altura, 0.1, 1000.0)
    mat_projection = np.array(mat_projection)    
    return mat_projection




def commands():


    # Define eventos do teclado
    def key_event(window,key,scancode,action,mods):
        
        global cameraPos, cameraFront, cameraUp, polygonal_mode

        cameraSpeed = 0.2
        if key == 87 and (action==1 or action==2): # tecla W
            cameraPos += cameraSpeed * cameraFront
        
        if key == 83 and (action==1 or action==2): # tecla S
            cameraPos -= cameraSpeed * cameraFront
        
        if key == 65 and (action==1 or action==2): # tecla A
            cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
            
        if key == 68 and (action==1 or action==2): # tecla D
            cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
            
        if key == 80 and action==1:
            polygonal_mode = not(polygonal_mode)

        global tx, ty

        if key == 265 and (action==1 or action==2): # tecla cima
            tx = tx-0.1
        
        if key == 264 and (action==1 or action==2): # tecla baixo
            tx = tx+0.1
        
        if key == 263 and (action==1 or action==2): # tecla esquerda
            ty = ty -0.1
            
        if key == 262 and (action==1 or action==2): # tecla direita
            ty = ty +0.1
        print('tx ty:',tx,ty)    
        print(key,scancode,action,mods)            
                     

    # Define eventos do mouse
    def mouse_event(window, xpos, ypos):
        
        global firstMouse, cameraFront, yaw, pitch, lastX, lastY

        if firstMouse:
            lastX = xpos
            lastY = ypos
            firstMouse = False

        xoffset = xpos - lastX
        yoffset = lastY - ypos
        lastX = xpos
        lastY = ypos

        sensitivity = 0.3 
        xoffset *= sensitivity
        yoffset *= sensitivity

        yaw += xoffset;
        pitch += yoffset;
        print('_____________________________')
        print('yaw pitch:',yaw,pitch)
        print('xpos ypos:',xpos,ypos)


        # CAMERA BUGA SE ANGULO DO PITCH FOR
        # >= 90   OU   <= -90
        if pitch >= 89.99: pitch = 89.99
        if pitch <= -89.99: pitch = -89.99


        front = glm.vec3()

        front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        front.y = math.sin(glm.radians(pitch))
        front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        cameraFront = glm.normalize(front)

    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, mouse_event)


