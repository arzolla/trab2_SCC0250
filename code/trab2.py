#!/usr/bin/env python3
#########################################
##### SCC0250 - Computação Gráfica ######
####### Trabalho 2 - Cenário 3D #########
#########################################
#### Aluno: Victor de Mattos Arzolla ####
#### NUSP: 9039312 ######################
#########################################


# Importando dependências
import glfw
from OpenGL.GL import *
#import OpenGL.GL.shaders
import numpy as np
import math
import glm
from PIL import Image
import sys, os
sys.path.append(os.path.join(sys.path[0],'sources'))

# Importa módulo com os codigos referentes aos shaders e buffer
import shader_buffer as sb
# Importa módulo com os codigos referentes aos comandos de teclado
import commands as cmd
import objects as obj


# inicializa o GLFW
if  glfw.init():
    print("GLFW Inicializado")
else:
    print("Erro na inicialização do GLFW")

# criando a janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
altura = 720
largura = 720
window = glfw.create_window(largura, altura, "Trabalho 2 - Cenário 3D", None, None)
glfw.make_context_current(window)


# Função para rodar shaders, retorna variavel programa principal
program = sb.run_shader()


#########################################
#########################################


glEnable(GL_TEXTURE_2D)
qtd_texturas = 10
textures = glGenTextures(qtd_texturas)






##############################################
##############################################


obj.declare_obj('caixa.obj','caixa2.jpg')

obj.declare_obj('terreno2.obj','pedra.jpg')

obj.declare_obj('casa.obj','casa.jpg')

obj.declare_obj('monstro.obj','monstro.jpg')



#########################################
#########################################

# Declara buffers da GPU e envia para shader_buffer.py
sb.buffer = glGenBuffers(2)

# Declara buffer de vertice
vertices = np.zeros(len(obj.vertices_list), [("position", np.float32, 3)])
vertices['position'] = obj.vertices_list

# Envia vértices para buffer
sb.vertex_buffer(vertices)


# Declara buffer de textura
textures = np.zeros(len(obj.textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
textures['position'] = obj.textures_coord_list

# Envia texturas para buffer
sb.texture_buffer(textures)


#########################################
#########################################

# Ativa os comandos de taclado e mouse
cmd.commands(window,altura,largura)

# Envia variável de programa para módulo objects.py
obj.program = program

#obj.vertex_index_main = vertex_index
#obj.texture_index_main = texture_index    


#########################################
#########################################


# Mostra a janela
glfw.show_window(window)
glfw.set_cursor_pos(window, cmd.lastX, cmd.lastY)

glEnable(GL_DEPTH_TEST) ### importante para 3D
   

rotacao_inc = 0


#########################################
#########################################


# Loop principal
while not glfw.window_should_close(window):

    glfw.poll_events() 
    
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if cmd.polygonal_mode==True:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    if cmd.polygonal_mode==False:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    

    obj.desenha_caixa()   
    obj.desenha_terreno()
    obj.desenha_casa()
    
    rotacao_inc += 0.1
    obj.desenha_monstro(rotacao_inc)
  

    
    mat_view = cmd.view(cmd.cameraPos, cmd.cameraFront, cmd.cameraUp)
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

    mat_projection = cmd.projection(altura,largura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)    
    
    

    
    glfw.swap_buffers(window)

glfw.terminate()