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
qtd_texturas = 30
textures = glGenTextures(qtd_texturas)

##############################################
################### OBJETOS ##################

# Declaração dos objetos a partir de modelo e texturas 

obj.declare_obj('chao.obj',['grass.jpg'])

obj.declare_obj('hut.obj',['body.jpg','frame.jpg','roof_floor.jpg'])

obj.declare_obj('pine_forest.obj',['pines.png','ground.jpeg'])

obj.declare_obj('tree.obj',['folhas.jpg','tronco.jpg'])

obj.declare_obj('skydome.obj',['milkyway.jpg'])

obj.declare_obj('spaceship.obj',['spaceship.jpg'])

obj.declare_obj('mothership.obj',['ms1.jpg','ms2.jpg','ms3.jpg','ms4.jpg','ms5.jpg'])

obj.declare_obj('remains.obj',['limb.jpg','body.jpg','skull.jpg','stones.jpg','sticks.jpg'])

obj.declare_obj('alien.obj',['blaster.jpg','alien.jpg'])

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

glEnable(GL_BLEND)
glEnable(GL_DEPTH_TEST) ### importante para 3D



rotacao_inc = 0
cameraPos   = cmd.cameraPos
cameraFront = cmd.cameraFront
cameraUp    = cmd.cameraUp

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
    
    

    # rotacao
    angle = rotacao_inc/10;
    r_x = 1.0; r_y = 1.0; r_z = 0.0;
    # translacao
    t_x = 0.0; t_y = -1.0; t_z = 0.0;
    # escala
    s_x = 800.0; s_y = 800.0; s_z = 800.0;

    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)


    obj.draw_obj('skydome.obj', mat_model)


    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    # translacao
    t_x = .0 ; t_y = 15.0; t_z = -15 +rotacao_inc/15;
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;

    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)


    obj.draw_obj('spaceship.obj', mat_model)
    


    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    # translacao
    t_x = 0.0 ; t_y = -2.0; t_z = 0.0;
    # escala

    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    
    obj.draw_obj('pine_forest.obj', mat_model)
    #obj.draw_obj('chao.obj', mat_model)


    s_x = 0.4; s_y = 0.4; s_z = 0.4;
    
    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    obj.draw_obj('remains.obj', mat_model)

    # translacao
    t_x = 0.4 ; t_y = -2.3; t_z = 0.0;
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    obj.draw_obj('tree.obj', mat_model)

    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    # translacao
    t_x = 5.5 ; t_y = -2 ; t_z = 2.2;
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    
    obj.draw_obj('hut.obj', mat_model)


    angle = -90.0;
    r_x = 0.0; r_y = 1.0; r_z = 0.0;

    s_x = 0.1; s_y = 0.1; s_z = 0.1;
    
    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)

    obj.draw_obj('alien.obj', mat_model)


    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    # translacao
    t_x = 400 ; t_y = 400.0; t_z = +200 -rotacao_inc/2;
    # escala
    s_x = 5.0; s_y = 5.0; s_z = 5.0;
    
    mat_model = obj.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)

    obj.draw_obj('mothership.obj', mat_model)
    
    rotacao_inc += 0.1
 
  
    #print('------------------')
    #print(cameraPos)
    #print(cameraUp)
    #print(cameraFront)

    
    cameraPos   = cameraPos
    cameraFront = cmd.cameraFront
    cameraUp    = cmd.cameraUp


    
    mat_view = obj.view(cameraPos, cameraFront, cameraUp)
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

    mat_projection = obj.projection(altura,largura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)    
    
    

    
    glfw.swap_buffers(window)

glfw.terminate()
