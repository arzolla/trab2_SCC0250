import numpy as np
import math as m
from OpenGL.GL import *


# Cores
cor_branco = [1,1,1] #
cor_preto = [0,0,0] #
cor_bg = [0.53,0.81,0.92] # Azul
cor_mato = [0.3,0.55,0.23] # verde
cor_rua = [0.5,0.5,0.5]
cor_carro = [1,0,0]
cor_calota = [0.7,0.7,0.7] #
cor_sol = [1,1,0] #
cor_faixa = [1,1,0] #
cor_sol2 = [1,0.6,0] #

# Classe de objetos tipo nuvem
num_vertices = 512 #      # define a resolução da nuvem


# Multiplicação de matrizes
def m_mult(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c


class Nuvem:

    # (Lembrar de enviar)
    program = 0     # variável para armazenar o programa principal
    loc = 0         # variável para armazenar variavel loc
    loc_color = 0   # variável para armazenar variavel loc_color

    # instancia uma Nuvel
    def __init__(self, index):

        self.index = index # index usado para desenhar nuvem
        pi = m.pi
        counter = 0
        radius = 1.0
        angle = 0.0

        # gera os vertices da nuvem
        self.coord = np.zeros(num_vertices, [("position", np.float32, 2)])
        for counter in range(num_vertices):
            angle += 2*pi/num_vertices
            x = (m.cos(angle) - m.sin(angle*24)/12)*radius
            y = (m.sin(angle) +  m.cos(angle*24)/12)*radius
            self.coord[counter] = [x*0.4,y*0.2]
        print(self.coord)

    # Função da classe para mover a nuvem no cenário
    def move(self,lista,off_x,off_y,x):

        mat = np.array([        1.0, 0.0, 0.0, off_x + x,
                                0.0, 1.0, 0.0, off_y,
                                0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 0.0, 1.0], np.float32)


        loc = glGetUniformLocation(Nuvem.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat)

        insert_obj(Nuvem.loc_color, lista, self.coord, self.index, cor_branco)

class Faixas:

    # (Lembrar de enviar)
    program = 0     # variável para armazenar o programa principal
    loc = 0         # variável para armazenar variavel loc
    loc_color = 0   # variável para armazenar variavel loc_color

    # instancia uma faixa
    def __init__(self, index):

        self.index = index # index usado para desenhar nuvem

        # gera os vertices da faixa
        self.coord = np.zeros(2, [("position", np.float32, 2)])
        self.coord["position"] = [
                                [0.3, -0.6],   # vertice 0
                                [-0.3, -0.6]   # vertice 1
                            ]
    # Função da classe para mover a faixa no cenário
    def move(self,lista,off_x,off_y,x,ceu_x):

        mat = np.array([        1.0, 0.0, 0.0, off_x +ceu_x,
                                0.0, 1.0, 0.0, off_y,
                                0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 0.0, 1.0], np.float32)


        loc = glGetUniformLocation(Faixas.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat)

        insert_line(Faixas.loc_color, lista, self.coord, self.index, cor_faixa)


class Sol:

    # (Lembrar de enviar)
    program = 0     # variável para armazenar o programa principal
    loc = 0         # variável para armazenar variavel loc
    loc_color = 0   # variável para armazenar variavel loc_color

    # instancia uma Nuvel
    def __init__(self):


        pi = m.pi
        counter = 0
        radius = 1.0
        angle = 0.0

        # gera os vertices da nuvem
        self.coord = np.zeros(num_vertices, [("position", np.float32, 2)])
        for counter in range(num_vertices):
            angle += 2*pi/num_vertices
            x = m.cos(angle)*radius
            y = m.sin(angle)*radius
            self.coord[counter] = [x*0.4,y*0.4]
        print(self.coord)
                # gera os vertices da nuvem
        self.raios = np.zeros(num_vertices, [("position", np.float32, 2)])
        for counter in range(num_vertices):
            angle += 2*pi/num_vertices
            x = m.cos(angle)*m.cos(12*angle)*radius
            y = m.sin(angle)*radius
            self.raios[counter] = [x*0.3,y*0.3]
        print(self.coord)



    # Função da classe para mover a nuvem no cenário
    def move(self,lista,off_x,off_y,x,y,scale):

        mat_t = np.array([        1.0, 0.0, 0.0, off_x + x,
                                0.0, 1.0, 0.0, off_y + y,
                                0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 0.0, 1.0], np.float32)


        mat_scale = np.array([  scale, 0.0, 0.0, 0.0,
                                0.0,scale, 0.0, 0.0,
                                0.0, 0.0, 1, 0.0,
                                0.0, 0.0, 0.0, 1], np.float32)

        mat = m_mult(mat_t,mat_scale)
        loc = glGetUniformLocation(Sol.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat)

        insert_obj(Sol.loc_color, lista, self.coord, 0, cor_sol)
        insert_line(Sol.loc_color, lista, self.raios, 0, cor_sol2)

def gen_mato():

    mato = np.zeros(4, [("position", np.float32, 2)])
    mato["position"] = [
                                [-1.1, -1.0],   # vertice 0
                                [1.1, -1.0],   # vertice 1
                                [1.1, -0.3] ,   # vertice 2
                                [-1.1, -0.3]    # vertice 3
                            ]

    return mato

def gen_rua():

    rua = np.zeros(4, [("position", np.float32, 2)])
    rua["position"] = [
                                [-1.1, -0.8],   # vertice 0
                                [1.1, -0.8],   # vertice 1
                                [1.1, -0.4] ,   # vertice 2
                                [-1.1, -0.4]    # vertice 3
                            ]

    return rua

class Carro():

    # (Lembrar de enviar)
    program = 0     # variável para armazenar o programa principal
    loc = 0         # variável para armazenar variavel loc
    loc_color = 0   # variável para armazenar variavel loc_color

    # instancia um carro
    def __init__(self):

        pi = m.pi
        counter = 0
        radius = 1.0
        angle = 0.0


        self.corpo = np.zeros(4, [("position", np.float32, 2)])
        self.corpo["position"] = [
                                    [-0.3, -0.1],   # vertice 0
                                    [0.3, -0.1],   # vertice 1
                                    [0.3, 0.1] ,   # vertice 2
                                    [-0.3, 0.1]    # vertice 3
                                ]

        self.corpo2 = np.zeros(4, [("position", np.float32, 2)])
        self.corpo2["position"] = [
                                    [-0.1, 0.1],   # vertice 0
                                    [0.1, 0.1],   # vertice 1
                                    [0.1, 0.2] ,   # vertice 2
                                    [-0.1, 0.2]    # vertice 3
                                ]

        # gera as rodas
        self.roda1 = np.zeros(num_vertices, [("position", np.float32, 2)])
        for counter in range(num_vertices):
            angle += 2*pi/num_vertices
            x = m.cos(angle)*radius
            y = m.sin(angle)*radius
            self.roda1[counter] = [x*0.07-0.2,y*0.07-0.1]

        self.calota1 = np.zeros(num_vertices, [("position", np.float32, 2)])
        for counter in range(num_vertices):
            angle += 2*pi/num_vertices
            x = m.cos(angle)*radius
            y = m.sin(angle)*radius
            self.calota1[counter] = [x*0.05-0.2,y*0.05-0.1]

        self.aro1 = np.zeros(4, [("position", np.float32, 2)])
        self.aro1["position"] = [
                                    [0.0-0.2, 0.05-0.1],   # vertice 0
                                    [0.0-0.2, -0.05-0.1],   # vertice 1
                                    [0.05-0.2, 0.0-0.1] ,   # vertice 2
                                    [-0.05-0.2, 0.0-0.1]    # vertice 3
                                ]

        self.roda2 = np.zeros(num_vertices, [("position", np.float32, 2)])
        for counter in range(num_vertices):
            angle += 2*pi/num_vertices
            x = m.cos(angle)*radius
            y = m.sin(angle)*radius
            self.roda2[counter] = [x*0.07+0.2,y*0.07-0.1]

        self.calota2 = np.zeros(num_vertices, [("position", np.float32, 2)])
        for counter in range(num_vertices):
            angle += 2*pi/num_vertices
            x = m.cos(angle)*radius
            y = m.sin(angle)*radius
            self.calota2[counter] = [x*0.05+0.2,y*0.05-0.1]

        self.aro2= np.zeros(4, [("position", np.float32, 2)])
        self.aro2["position"] = [
                                    [0.0+0.2, 0.05-0.1],   # vertice 0
                                    [0.0+0.2, -0.05-0.1],   # vertice 1
                                    [0.05+0.2, 0.0-0.1] ,   # vertice 2
                                    [-0.05+0.2, 0.0-0.1]    # vertice 3
                                ]

    # Funrção da classe para mover o carro
    def move(self,lista,off_x,off_y,x,y,ceu_x):

        center_x = -0.2
        center_y = -0.1
        mat_corpo = np.array([  1.0, 0.0, 0.0, off_x + x,
                                0.0, 1.0, 0.0, off_y + y,
                                0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 0.0, 1.0], np.float32)

        mat_rotation = np.array([   m.cos(-2*m.pi*(x-ceu_x)), -m.sin(-2*m.pi*(x-ceu_x)), 0.0, 0.0,
                            m.sin(-2*m.pi*(x-ceu_x)), m.cos(-2*m.pi*(x-ceu_x)), 0.0, 0.0,
                            0.0, 0.0, 1.0, 0.0,
                            0.0, 0.0, 0.0, 1.0], np.float32)

        mat_posi1 = np.array([       1.0, 0.0, 0.0,  + center_x,
                                    0.0, 1.0, 0.0,  + center_y,
                                    0.0, 0.0, 1.0, 0.0,
                                    0.0, 0.0, 0.0, 1.0], np.float32)

        mat_posi_m1 = np.array([     1.0, 0.0, 0.0, -center_x,
                                    0.0, 1.0, 0.0, -center_y,
                                    0.0, 0.0, 1.0, 0.0,
                                    0.0, 0.0, 0.0, 1.0], np.float32)

        mat_posi2 = np.array([       1.0, 0.0, 0.0, - center_x,
                                    0.0, 1.0, 0.0, + center_y,
                                    0.0, 0.0, 1.0, 0.0,
                                    0.0, 0.0, 0.0, 1.0], np.float32)

        mat_posi_m2 = np.array([     1.0, 0.0, 0.0, +center_x,
                                    0.0, 1.0, 0.0, -center_y,
                                    0.0, 0.0, 1.0, 0.0,
                                    0.0, 0.0, 0.0, 1.0], np.float32)

        mat_aro1 = m_mult(mat_corpo,m_mult(mat_posi1,m_mult(mat_rotation,mat_posi_m1)))
        mat_aro2 = m_mult(mat_corpo,m_mult(mat_posi2,m_mult(mat_rotation,mat_posi_m2)))
        loc = glGetUniformLocation(Carro.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_corpo)
        insert_obj(Carro.loc_color,lista,self.corpo,0,cor_carro)
        insert_obj(Carro.loc_color,lista,self.corpo2,0,cor_carro)
        insert_obj(Carro.loc_color,lista,self.roda1,0,cor_preto)
        insert_obj(Carro.loc_color,lista,self.roda2,0,cor_preto)
        insert_obj(Carro.loc_color,lista,self.calota1,0,cor_calota)
        insert_obj(Carro.loc_color,lista,self.calota2,0,cor_calota)

        loc = glGetUniformLocation(Carro.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_aro1)
        insert_line(Carro.loc_color,lista,self.aro1,0,cor_preto)

        loc = glGetUniformLocation(Carro.program, "mat_transformation")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_aro2)
        insert_line(Carro.loc_color,lista,self.aro2,0,cor_preto)

def insert_obj(loc_color, lista, objeto, index, cor):
    offset = 0
    #print('objeto:',objeto)
    #pos = lista.index(objeto)
    pos = []
    for i in range(len(lista)):
        if len(objeto) == len(lista[i]):
            if (objeto == lista[i]).all(): pos.append(i)

    for i in range(pos[index]):
        offset = offset + len(lista[i])

    # Desenha objeto
    glUniform4f(loc_color, *cor, 1.0) # cor
    glDrawArrays(GL_TRIANGLE_FAN, offset,len(objeto)) # desenha objeto
    glUniform4f(loc_color, *cor_preto, 1.0) # preto
    glDrawArrays(GL_LINE_LOOP, offset,len(objeto)) # desenha linha

def insert_line(loc_color, lista, objeto, index, cor):
    offset = 0
    #print('objeto:',objeto)
    #pos = lista.index(objeto)
    pos = []
    for i in range(len(lista)):
        if len(objeto) == len(lista[i]):
            if (objeto == lista[i]).all(): pos.append(i)

    for i in range(pos[index]):
        offset = offset + len(lista[i])

    # Desenha objeto
    glUniform4f(loc_color, *cor, 1.0) # preto
    glDrawArrays(GL_LINES, offset,len(objeto)) # desenha linha

    # instancia um carro

def gen_carro():
    aa = np.zeros(4, [("position", np.float32, 2)])
    aa["position"] = [
                                    [-0.3, -0.1],   # vertice 0
                                    [0.3, -0.1],   # vertice 1
                                    [0.3, 0.1] ,   # vertice 2
                                    [-0.3, 0.1]    # vertice 3
                            ]
    return aa
