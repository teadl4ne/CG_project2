from OpenGL.GL import *
import glm

VERTEX = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTex;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec3 FragPos;
out vec3 Normal;
out vec2 TexCoord;

void main() {
    FragPos = vec3(model * vec4(aPos,1.0));
    Normal = mat3(transpose(inverse(model))) * aNormal;
    TexCoord = aTex;
    gl_Position = proj * view * vec4(FragPos,1.0);
}
"""

FRAGMENT = """
#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

uniform sampler2D noiseTex;
uniform vec3 viewPos;

uniform vec3 lightPos1;
uniform vec3 lightColor1;
uniform vec3 lightPos2;
uniform vec3 lightColor2;

uniform vec3 baseColor;
uniform bool emissive;
uniform float time;

void main() {
    vec2 uv = TexCoord * 2.0 + vec2(time, time * 0.5);
    vec3 noise = texture(noiseTex, uv).rgb;
    vec3 color = baseColor * noise;

    if (emissive) {
        FragColor = vec4(color * 2.0, 1.0);
        return;
    }

    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    vec3 result = vec3(0.05);

    vec3 lights[2] = vec3[](lightPos1, lightPos2);
    vec3 colors[2] = vec3[](lightColor1, lightColor2);

    for (int i = 0; i < 2; i++) {
        vec3 lightDir = normalize(lights[i] - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        result += (diff + spec) * colors[i];
    }

    FragColor = vec4(result * color, 1.0);
}
"""

class Shader:
    def __init__(self):
        self.ID = glCreateProgram()
        self._compile()

    def _compile(self):
        v = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(v, VERTEX)
        glCompileShader(v)

        f = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(f, FRAGMENT)
        glCompileShader(f)

        glAttachShader(self.ID, v)
        glAttachShader(self.ID, f)
        glLinkProgram(self.ID)

        glDeleteShader(v)
        glDeleteShader(f)

    def use(self):
        glUseProgram(self.ID)

    def set_mat4(self, name, m):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(m))

    def set_vec3(self, name, v):
        glUniform3f(glGetUniformLocation(self.ID, name), v.x, v.y, v.z)

    def set_float(self, name, v):
        glUniform1f(glGetUniformLocation(self.ID, name), v)

    def set_int(self, name, v):
        glUniform1i(glGetUniformLocation(self.ID, name), v)

    def set_bool(self, name, v):
        glUniform1i(glGetUniformLocation(self.ID, name), int(v))
