from OpenGL.GL import *
import glfw
import math as m

# flags de tecla
f_carro_ya = 0
f_carro_xa = 0
f_carro_yb = 0
f_carro_xb = 0
f_ceu_x  =0
f_sol_s  =0

program = 0


# Variáveis das transformações
angulo = 0
ceu_x = 0.0
carro_x = 0.0
carro_y = 0.0


# Função para ler comandos de teclado, retorna variaveis da transformação
def run_key_commands(window):

    #função para evento de botão de teclado
    def key_event(window,key,scancode,action,mods):
        print('[key events]')
        print('{:<7}{:<7}{:<7}{:<7}'.format('key','code','action','mods'))
        print('{:<7}{:<7}{:<7}{:<7}'.format(key,scancode,action,mods))
        print('------')
        global ceu_x, carro_x, carro_y, angulo, f_ceu_x,f_sol_s

        if key == 32 and (action == 1): f_ceu_x = not f_ceu_x # Space
        print(f_ceu_x)

        global f_carro_ya, f_carro_yb, f_carro_xa, f_carro_xb
        if key == 87 and (action != 0): f_carro_ya = 1 # W
        else: f_carro_ya = 0 # W
        if key == 65 and (action != 0): f_carro_xa = 1 # A
        else: f_carro_xa = 0 # A
        if key == 83 and (action != 0): f_carro_yb = 1 # S
        else: f_carro_yb = 0 # S
        if key == 68 and (action != 0): f_carro_xb = 1 # D
        else: f_carro_xb = 0 # D

        if key == 67 and (action != 0): f_sol_s = 1 # C
        else: f_sol_s = 0 # C



    glfw.set_key_callback(window,key_event)



