vert_txt = """
#version 130

uniform mat4 modelMatrix;

varying vec3 fNormal;
varying vec3 fPosition;
varying vec3 fColor;

void main ()
{
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    fPosition = vec3(modelMatrix * gl_Vertex);
    fColor = vec3(gl_Color);
    fNormal = normalize(mat3(modelMatrix) * gl_Normal);
}
"""

frag_txt = """
#version 130

out vec4 FragColor;

uniform vec3 cameraPos;
uniform uint iLights;

varying vec3 fNormal;
varying vec3 fPosition;
varying vec3 fColor;

#define STEPS 2
#define CONTOUR_THICKNESS 8.8  // [0, 10]

float attenuation(int light_index, vec3 light_dir){
    float d = abs(length(light_dir));
    float attenuation = gl_LightSource[light_index].constantAttenuation;
    attenuation += gl_LightSource[light_index].linearAttenuation * d;
    attenuation += gl_LightSource[light_index].quadraticAttenuation * pow(d, 2);
    attenuation = 1. / attenuation;
    return attenuation;
}

void main()
{

    vec3 ambient_color  = 0.3  * fColor;
    vec3 final_color = vec3(0., 0., 0.);

    vec3 v = normalize(cameraPos - fPosition);
    vec3 n = normalize(fNormal);

    for (int l_idx = 0; l_idx < int(iLights); l_idx++){
        vec3 light_dir = vec3(gl_LightSource[l_idx].position) - fPosition;
        vec3 l = normalize(light_dir);
        vec3 h = (v + l) / length(v + l);

        float spot = (1. - dot(-l, gl_LightSource[l_idx].spotDirection)) * 90.;
        spot = max(sign(gl_LightSource[l_idx].spotCutoff - spot), 0.);

        float diffuse_factor = round(max(0.0, dot(n, l)) * STEPS) / STEPS;
        vec3 diffuse_color = 0.3 * diffuse_factor * vec3(gl_LightSource[l_idx].diffuse);
        float specular_factor = round(pow(max(0.0, dot(n, h)), 64) * STEPS) / STEPS ;
        vec3 specular_color = 0.5 * specular_factor * vec3(gl_LightSource[l_idx].specular);

        final_color += (spot * (diffuse_color + specular_color) + ambient_color / iLights) * attenuation(l_idx, light_dir);
    }

    // draw black contour; value is either 0. or 1.
    float contour_factor = min(round((10. - CONTOUR_THICKNESS) * dot(v, n)), 1.);
    FragColor = vec4(final_color * contour_factor, 1.);
}
"""