#!/usr/bin/env python3
#########################################
##### SCC0250 - Computação Gráfica ######
##### Trabalho 1 - Transformação 2D #####
#########################################
#### Aluno: Victor de Mattos Arzolla ####
#### NUSP: 9039312 ######################
#########################################


# Importando dependências
import glfw
from OpenGL.GL import *
#import OpenGL.GL.shaders
import numpy as np
import math as m
import sys, os
sys.path.append(os.path.join(sys.path[0],'sources'))


# Importa módulo com os codigos referentes aos shaders e buffer
from shader_buffer import *
# Importa módulo com os codigos referentes aos comandos de teclado
import key_commands as key_c
from objects import *


# inicializa o GLFW
if  glfw.init():
    print("GLFW Inicializado")
else:
    print("Erro na inicialização do GLFW")

# criando a janela
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(720, 720, "Janela", None, None)
glfw.make_context_current(window)



# Função para rodar shaders, retorna variavel programa principal
program = run_shader()


#########################################
#########################################


# Instanciação dos vértices
mato = gen_mato()
rua = gen_rua()
carro = Carro()
nuvem0 = Nuvem(0)
nuvem1 = Nuvem(1)
nuvem2 = Nuvem(2)
nuvem3 = Nuvem(3)
nuvem4 = Nuvem(4)
nuvem5 = Nuvem(5)
sol = Sol()
faixa0=Faixas(0)

faixa = []
for i in range(10):
    faixa.append(Faixas(i))


lista = [nuvem0.coord,nuvem1.coord,mato,rua,carro.corpo,carro.roda1,carro.roda2,
carro.calota1,carro.calota2,carro.aro1,carro.aro2,sol.coord,sol.raios,carro.corpo2,
faixa[0].coord,faixa[1].coord,faixa[2].coord,faixa[3].coord,faixa[4].coord,
faixa[5].coord,faixa[6].coord,faixa[7].coord,faixa[8].coord,faixa[9].coord
]
# Concatena os vertices para enviar ao buffer
vertices = np.concatenate((lista))



#########################################
#########################################


# Roda os buffers, recebe programa e os vertices e retorna loc e loc_color
loc, loc_color = run_buffer(program, vertices)

# Mostra a janela
glfw.show_window(window)

# Ativa os comandos do teclado
key_c.run_key_commands(window)


# Envia para classes as variáveis de programa, loc e loc_color
Nuvem.program = program
Nuvem.loc = loc
Nuvem.loc_color = loc_color

Carro.program = program
Carro.loc = loc
Carro.loc_color = loc_color

Sol.program = program
Sol.loc = loc
Sol.loc_color = loc_color

Faixas.program = program
Faixas.loc = loc
Faixas.loc_color = loc_color


# inicialização de variaveis
carro_x = 0
carro_y = 0
ceu_x = 0
ceu_y = 0
ceu_alt_x = 0
escala_sol = 1
#key_c.program = program
cont_faixa = 0

# Loop principal
while not glfw.window_should_close(window):

    #
    glfw.poll_events()




    # comparações para restringir os limites dos comandos
    if escala_sol < 2:
        escala_sol = escala_sol + 0.001*key_c.f_sol_s

    ceu_x = ceu_x - 0.0005
    ceu_alt_x = ceu_alt_x - 0.015*key_c.f_ceu_x
    ceu_x = ceu_x - 0.001*key_c.f_ceu_x # SPACE
    ceu_y = ceu_y + 0.0005

    if  carro_y > 0:
        carro_y = carro_y - (0.01*key_c.f_carro_yb)*key_c.f_ceu_x # S, depende de SPACE apertado

    if carro_y < 0.4:
        carro_y = carro_y + (0.01*key_c.f_carro_ya)*key_c.f_ceu_x # W, depende de SPACE apertado

    if  carro_x > 0:
        carro_x = carro_x - 0.01*key_c.f_carro_xa # A
    if carro_x < 1.4:
        carro_x = carro_x + 0.01*key_c.f_carro_xb # D



    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(*cor_bg, 1.0)

    # matriz identidade
    mat_id = np.array([             1.0, 0.0, 0.0, 0.0,
                                    0.0, 1.0, 0.0, 0.0,
                                    0.0, 0.0, 1.0, 0.0,
                                    0.0, 0.0, 0.0, 1.0], np.float32)


    # Desenha o sol
    sol.move(lista,0,0,0,ceu_y,escala_sol)

    # Cenário
    loc = glGetUniformLocation(program, "mat_transformation")
    glUniformMatrix4fv(loc, 1, GL_TRUE, mat_id)


   # Desenha mato
    insert_obj(loc_color,lista,mato,0,cor_mato)

    # Desenha rua
    insert_obj(loc_color,lista,rua,0,cor_rua)



    # Dexenha todas as faixas
    for i in range(len(faixa)):

        faixa[i].move(lista,cont_faixa,0,carro_x,ceu_alt_x)
        cont_faixa = cont_faixa+0.8
    cont_faixa = 0



    # insere o carro
    carro.move(lista,-0.7,-0.630 ,carro_x,carro_y,ceu_alt_x)
    # insere nuvem
    nuvem0.move(lista,0.3,0.3,ceu_x)
    nuvem1.move(lista,-0.6,0.6,ceu_x)


    glfw.swap_buffers(window)

glfw.terminate()
