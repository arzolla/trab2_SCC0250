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
#import objects as obj


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


# Instanciação dos vértices

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue


        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])


        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model


glEnable(GL_TEXTURE_2D)
qtd_texturas = 10
textures = glGenTextures(qtd_texturas)

def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    img_width = img.size[0]
    img_height = img.size[1]
    image_data = img.tobytes("raw", "RGB", 0, -1)
    #image_data = np.array(list(img.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)


vertices_list = []    
textures_coord_list = []

def obj_path(obj):
    path = os.path.join(sys.path[0],'models',obj)
    return path

def tex_path(tex):
    path = os.path.join(sys.path[0],'textures',tex)
    return path


modelo = load_model_from_file(obj_path('caixa.obj'))

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo cube.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo cube.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas


### carregando textura equivalente e definindo um id (buffer): use um id por textura!
load_texture_from_file(0,tex_path('caixa2.jpg'))


modelo = load_model_from_file(obj_path('terreno2.obj'))

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo terreno.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo terreno.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas


### carregando textura equivalente e definindo um id (buffer): use um id por textura!
load_texture_from_file(1,tex_path('pedra.jpg'))

modelo = load_model_from_file(obj_path('casa.obj'))

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo casa.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo casa.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas


### carregando textura equivalente e definindo um id (buffer): use um id por textura!
load_texture_from_file(2,tex_path('casa.jpg'))


modelo = load_model_from_file(obj_path('monstro.obj'))

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo monstro.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo monstro.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas


### carregando textura equivalente e definindo um id (buffer): use um id por textura!
load_texture_from_file(3,tex_path('monstro.jpg'))





#########################################
#########################################


# Roda buffer de vertice
vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
vertices['position'] = vertices_list

loc_vertices = sb.vertex_buffer(program, vertices)


# Roda buffer de textura
textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
textures['position'] = textures_coord_list

loc_texture_coord = sb.texture_buffer(program,textures)


#########################################
#########################################



def desenha_caixa():
    
    
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
    glBindTexture(GL_TEXTURE_2D, 0)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 0, 36) ## renderizando
    

def desenha_terreno():
    
    
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
    glBindTexture(GL_TEXTURE_2D, 1)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 36, 42-36) ## renderizando



def desenha_casa():
    
    
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
    glBindTexture(GL_TEXTURE_2D, 2)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 42, 1476-42) ## renderizando


def desenha_monstro(rotacao_inc):
    
    
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
    glBindTexture(GL_TEXTURE_2D, 3)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 1476, 7584-1476) ## renderizando


#########################################
#########################################


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
    
    

    desenha_caixa()   
    desenha_terreno()
    desenha_casa()
    
    rotacao_inc += 0.1
    desenha_monstro(rotacao_inc)
  

    
    mat_view = cmd.view(cmd.cameraPos, cmd.cameraFront, cmd.cameraUp)
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_FALSE, mat_view)

    mat_projection = cmd.projection(altura,largura)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_FALSE, mat_projection)    
    
    

    
    glfw.swap_buffers(window)

glfw.terminate()