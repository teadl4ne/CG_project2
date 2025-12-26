#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

uniform vec3 viewPos;

uniform vec3 lightPos1;
uniform vec3 lightPos2;
uniform bool light1On;
uniform bool light2On;

uniform vec3 baseColor;
uniform sampler2D tex;
uniform float time;
uniform bool emissive;

vec3 applyLight(vec3 lightPos, vec3 color)
{
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);

    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);

    return (diff + spec * 0.5) * color;
}

void main()
{
    vec2 uv = FragPos.xz * 0.2 + vec2(time);
    float noise = texture(tex, uv).r;
    vec3 color = baseColor * (0.4 + 0.6 * noise);

    vec3 lighting = vec3(0.2) * color;

    if (light1On)
        lighting += applyLight(lightPos1, vec3(1.0, 0.9, 0.7));

    if (light2On)
        lighting += applyLight(lightPos2, vec3(0.4, 0.6, 1.0));

    if (emissive)
        lighting = color * 3.0;

    FragColor = vec4(lighting, 1.0);
}
