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


vertices_list = []    
textures_coord_list = []

texture_index = {
    # 'textura' : id_textura
}

vertex_index = {
    # 'modelo' : [inicial, final]
}

##############################################



##############################################

vertex_index, texture_index = obj.declare_obj(obj.vertices_list,'caixa.obj','caixa2.jpg',vertex_index, texture_index)

vertex_index, texture_index = obj.declare_obj(obj.vertices_list,'terreno2.obj','pedra.jpg',vertex_index, texture_index)

vertex_index, texture_index = obj.declare_obj(obj.vertices_list,'casa.obj','casa.jpg',vertex_index, texture_index)

vertex_index, texture_index = obj.declare_obj(obj.vertices_list,'monstro.obj','monstro.jpg',vertex_index, texture_index)







#########################################
#########################################


# Roda buffer de vertice
vertices = np.zeros(len(obj.vertices_list), [("position", np.float32, 3)])
vertices['position'] = obj.vertices_list

loc_vertices = sb.vertex_buffer(program, vertices)


# Roda buffer de textura
textures = np.zeros(len(obj.textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
textures['position'] = obj.textures_coord_list

loc_texture_coord = sb.texture_buffer(program,textures)


#########################################
#########################################



def desenha_caixa(vertex_index, texture_index):
    
    
    # aplica a matriz model
    
    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    
    # translacao
    t_x = 0.0; t_y = 0.0; t_z = 15.0;
    
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, texture_index['caixa2.jpg'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, vertex_index['caixa.obj'][0], vertex_index['caixa.obj'][1]) ## renderizando
    

def desenha_terreno(vertex_index, texture_index):
    
    
    # aplica a matriz model
    
    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    
    # translacao
    t_x = 0.0; t_y = -1.01; t_z = 0.0;
    
    # escala
    s_x = 20.0; s_y = 20.0; s_z = 20.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, texture_index['pedra.jpg'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, vertex_index['terreno2.obj'][0], vertex_index['caixa.obj'][1]) ## renderizando
    


def desenha_casa(vertex_index, texture_index):
    
    
    # aplica a matriz model
    
    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    
    # translacao
    t_x = 0.0; t_y = -1.0; t_z = 0.0;
    
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, texture_index['casa.jpg'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, vertex_index['casa.obj'][0], vertex_index['caixa.obj'][1]) ## renderizando
    


def desenha_monstro(vertex_index, texture_index, rotacao_inc):
    
    
    # aplica a matriz model
    
    # rotacao
    angle = rotacao_inc;
    r_x = 0.0; r_y = 1.0; r_z = 0.0;
    
    # translacao
    t_x = 0.0; t_y = -1.0; t_z = 0.0;
    
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
 #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, texture_index['monstro.jpg'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, vertex_index['monstro.obj'][0], vertex_index['caixa.obj'][1]) ## renderizando
    


#########################################
#########################################

# Ativa os comandos de taclado e mouse
cmd.commands(window,altura,largura)



    



#########################################
#########################################

def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

    
    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform).T # pegando a transposta da matriz (glm trabalha com ela invertida)
    
    return matrix_transform




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
    
    

    desenha_caixa(vertex_index, texture_index)   
    desenha_terreno(vertex_index, texture_index)
    desenha_casa(vertex_index, texture_index)
    
    rotacao_inc += 0.1
    desenha_monstro(vertex_index, texture_index, rotacao_inc)
  

    
    mat_view = cmd.view(cmd.cameraPos, cmd.cameraFront, cmd.cameraUp)
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

    mat_projection = cmd.projection(altura,largura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)    
    
    

    
    glfw.swap_buffers(window)

glfw.terminate()