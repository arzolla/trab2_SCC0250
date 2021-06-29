import glm
import glfw
import math
import numpy as np

cameraPos   = glm.vec3(0.0,  0.0,  1.0);
cameraFront = glm.vec3(0.0,  0.0, -1.0);
cameraUp    = glm.vec3(0.0,  1.0,  0.0);


polygonal_mode = False

firstMouse = True
yaw = -90.0 
pitch = 0.0

# Instancia variaveis
lastX =  []
lastY =  []

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
 
            
                     

    # Define eventos do mouse
    def mouse_event(window, xpos, ypos):
        
        global firstMouse, cameraFront, yaw, pitch, lastX, lastY
        global altura, largura

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

        
        if pitch >= 90.0: pitch = 90.0
        if pitch <= -90.0: pitch = -90.0

        front = glm.vec3()
        front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        front.y = math.sin(glm.radians(pitch))
        front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
        cameraFront = glm.normalize(front)

    glfw.set_key_callback(window, key_event)
    glfw.set_cursor_pos_callback(window, mouse_event)


