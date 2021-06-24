from OpenGL.GL import *

# Código do shader de vértice
vertex_code = """
        attribute vec2 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,0.0,1.0);
        }
        """

# Código do shader de fragmento
fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """
fragment_code1 = """

        uniform vec4 color;
        void main(){
            vec2 screen_size = vec2(720,720);
            vec3 cor1 = vec3(1.0,0.0,0.0);
            vec3 cor2 = vec3(0.0,0.0,1.0);
            vec2 xy = gl_FragCoord.xy/screen_size;

            float mix_valor = distance(xy,vec2(0,1));
            vec3 cor_gradient = mix(cor1,cor2,mix_valor);

            gl_FragColor = vec4(cor_gradient,1);
        }
        """



# Programa para declarar programa principal e configurar shaders
def run_shader():

    # Requisitando slot para a GPU para os programas Vertex e Fragment Shaders
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # Associando código-fonte aos slots solicitados
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # Compilando o Vertex Shader
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Vertex Shader")

    # Compilando o Fragment Shader
    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Fragment Shader")


    # Associando os programas compilado ao programa principal
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    # Build program
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')

    # Seta como programa padrão
    glUseProgram(program)

    return program

def run_buffer(program, vertices):

    # Request a buffer slot from GPU
    buffer = glGenBuffers(1)
    # Make this buffer the default one
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # Upload data
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # Bind the position attribute
    # --------------------------------------
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)

    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

    loc_color = glGetUniformLocation(program, "color")

    return loc, loc_color






