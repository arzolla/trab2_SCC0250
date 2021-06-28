from OpenGL.GL import *
import numpy as np
import math
import glm
from PIL import Image
import sys, os


##############################################
############# FUNÇÕES AUXILIARES #############
##############################################

# Função para carregar modelo a partir de arquivo .obj
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

# Função para carregar a textura a partir de arquivo de imagem
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
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

# Acesso aos paths de modelos e texturas
def mod_path(obj):
    path = os.path.join(sys.path[0],'sources','models',obj)
    return path

def tex_path(tex):
    path = os.path.join(sys.path[0],'sources','textures',tex)
    return path

# Matriz model
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

# Matriz view
def view(cameraPos, cameraFront, cameraUp):

    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

# Matriz projection
def projection(altura,largura):

    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(45.0), largura/altura, 0.1, 1000.0)
    mat_projection = np.array(mat_projection)    
    return mat_projection


##############################################
################### OBJETOS ##################
##############################################


# Lista de vertices e coordenadas da textura
vertices_list = []    
textures_coord_list = []

# Dicionário para armazenar o indice da textura 
texture_index = {
    # 'modelo' : id_textura
}
# Dicionário para armazenar inicio e fim dos vértices 
vertex_index = {
    # 'modelo' : [vertice_inicial, numero_vertices]
}
### Para facilidade, as chaves de ambos são o nome do modelo


# Função para declarar os objetos
def declare_obj(model, texture):
    
    global vertex_index, texture_index
    modelo = load_model_from_file(mod_path(model))

    ### inserindo vertices do modelo no vetor de vertices
    print('Processando modelo ',model,'. Vertice inicial:',len(vertices_list))
    vertex_index[model] = [len(vertices_list), -len(vertices_list)]
    for face in modelo['faces']:
        for vertice_id in face[0]:
            vertices_list.append( modelo['vertices'][vertice_id-1] )
        for texture_id in face[1]:
            textures_coord_list.append( modelo['texture'][texture_id-1] )
    print('Processando modelo ',model,'. Vertice final:',len(vertices_list))
    vertex_index[model][1] += len(vertices_list)

    ### inserindo coordenadas de textura do modelo no vetor de texturas

    ### carregando textura equivalente e definindo um id (buffer)
    print('indice da textura do',texture ,':',len(texture_index))
    texture_index[model] = len(texture_index)
    load_texture_from_file(texture_index[model],tex_path(texture))



# Variável instanciada para armazenar programa principal
program = []



# aplica a matriz model

# rotacao
angle = 0.0;
r_x = 0.0; r_y = 0.0; r_z = 1.0;

# translacao
t_x = 0.0; t_y = 0.0; t_z = 15.0;

# escala
s_x = 1.0; s_y = 1.0; s_z = 1.0;

mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)


def draw_obj(modelo):

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
    glBindTexture(GL_TEXTURE_2D, texture_index[modelo])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, *vertex_index[modelo]) ## renderizando




def desenha_caixa():
    
    
    
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, texture_index['caixa.obj'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, *vertex_index['caixa.obj']) ## renderizando
    

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
    glBindTexture(GL_TEXTURE_2D, texture_index['terreno2.obj'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, *vertex_index['terreno2.obj']) ## renderizando
    


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
    glBindTexture(GL_TEXTURE_2D, texture_index['casa.obj'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, *vertex_index['casa.obj'])


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
    glBindTexture(GL_TEXTURE_2D, texture_index['monstro.obj'])
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, *vertex_index['monstro.obj'])
