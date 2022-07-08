vert_txt = """
#version 130
uniform mat4 modelMatrix;
uniform vec3 cameraPos;
uniform uint iLights;

varying vec3 fcolor;

float attenuation(int light_index, vec3 light_dir){
    float d = abs(length(light_dir));
    float attenuation = gl_LightSource[light_index].constantAttenuation;
    attenuation += gl_LightSource[light_index].linearAttenuation * d;
    attenuation += gl_LightSource[light_index].quadraticAttenuation * pow(d, 2);
    attenuation = 1. / attenuation;
    return attenuation;
}

void main ()
{
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    vec3 vPosition = vec3(modelMatrix * gl_Vertex);

    vec3 ambient_color  = 0.3  * vec3(gl_Color);
    vec3 final_color = vec3(0., 0., 0.);

    vec3 v = normalize(cameraPos - vPosition);
    vec3 n = normalize(mat3(modelMatrix) * gl_Normal);
    for (int l_idx = 0; l_idx < int(iLights); l_idx++){
        vec3 light_dir = vec3(gl_LightSource[l_idx].position) - vPosition;
        vec3 l = normalize(light_dir);
        vec3 h = (v + l) / length(v + l);

        float spot = (1. - dot(-l, gl_LightSource[l_idx].spotDirection)) * 90.;
        spot = max(sign(gl_LightSource[l_idx].spotCutoff - spot), 0.);

        vec3 diffuse_color = 0.3 * max(0.0, dot(n, l)) * vec3(gl_LightSource[l_idx].diffuse);
        vec3 specular_color = 0.5 * pow(max(0.0, dot(n, h)), 64) * vec3(gl_LightSource[l_idx].specular);

        final_color += (spot * (diffuse_color + specular_color) + ambient_color / iLights) * attenuation(l_idx, light_dir);
    }

    fcolor = final_color;
}

"""

frag_txt = """
#version 130

out vec4 FragColor;

varying vec3 fcolor;

void main()
{
    FragColor = vec4(fcolor, 1.);
}
"""