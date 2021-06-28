#!/usr/bin/env python37
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

# Declarando a janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
largura = 1280
altura = 720
window = glfw.create_window(largura, altura, "Trabalho 2 - Cenário 3D", None, None)
glfw.make_context_current(window)


##############################################
##############################################

# Função para rodar shaders, retorna variavel programa principal
program = sb.run_shader()

# Configura suporte a texturas
glEnable(GL_TEXTURE_2D)
qtd_texturas = 10
textures = glGenTextures(qtd_texturas)

##############################################
################### OBJETOS ##################

# Declaração dos objetos a partir de modelo e textura
#obj.declare_obj('caixa.obj','caixa2.jpg')

obj.declare_obj('terreno2.obj','pedra.jpg')

obj.declare_obj('casa.obj','casa.jpg')

obj.declare_obj('monstro.obj','monstro.jpg')

obj.declare_obj('carro.obj','pedra.jpg')

obj.declare_obj('spaceship.obj','spaceship.jpg')

# Envia variável de programa para módulo objects.py
obj.program = program

##############################################
################### BUFFERS ##################

# Declara buffers da GPU e envia para módulo shader_buffer.py
sb.buffer = glGenBuffers(2)

# Declara variável para armazenar lista de vértices
vertices = np.zeros(len(obj.vertices_list), [("position", np.float32, 3)])
# Obtém lista de vértices do módulo objetcs.py
vertices['position'] = obj.vertices_list

# Envia lista de vértices para buffer da GPU
sb.vertex_buffer(vertices)


# Declara variável para armazenar lista de coordenadas de textura
textures = np.zeros(len(obj.textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
# Obtém lista de coordenadas de textura do módulo objetcs.py
textures['position'] = obj.textures_coord_list

# Envia lista de coordenadas de texturas para buffer da GPU
sb.texture_buffer(textures)

##############################################
################### COMANDOS #################

# Envia variáveis de janela para modulo commands.py
cmd.lastX =  largura/2
cmd.lastY =  altura/2
cmd.window = window
# Ativa os comandos de teclado e mouse
cmd.commands()


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
    
    
    #obj.desenha_caixa()   
    obj.desenha_terreno()
    obj.draw_obj('casa.obj')
    #obj.draw_obj('carro.obj')
    obj.draw_obj('spaceship.obj')

    rotacao_inc += 0.1
    #obj.desenha_monstro(rotacao_inc)
    #obj.desenha_monstro(-rotacao_inc)
  

    
    mat_view = obj.view(cmd.cameraPos, cmd.cameraFront, cmd.cameraUp)
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

    mat_projection = obj.projection(altura,largura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)    
    
    

    
    glfw.swap_buffers(window)

glfw.terminate()