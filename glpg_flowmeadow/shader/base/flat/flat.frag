#version 130

out vec4 FragColor;

uniform vec3 cameraPos;
uniform uint iLights;
varying vec3 fPosition;
varying vec3 fColor;

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

    vec3 xTangent = dFdx(fPosition);
    vec3 yTangent = dFdy(fPosition);
    vec3 n = normalize(cross(xTangent, yTangent));
    vec3 v = normalize(cameraPos - fPosition);

    for (int l_idx = 0; l_idx < int(iLights); l_idx++){
        vec3 light_dir = vec3(gl_LightSource[l_idx].position) - fPosition;
        vec3 l = normalize(light_dir);
        vec3 h = (v + l) / length(v + l);

        float spot = (1. - dot(-l, gl_LightSource[l_idx].spotDirection)) * 90.;
        spot = max(sign(gl_LightSource[l_idx].spotCutoff - spot), 0.);

        vec3 diffuse_color = 0.3 * max(0.0, dot(n, l)) * vec3(gl_LightSource[l_idx].diffuse);
        vec3 specular_color = 0.5 * pow(max(0.0, dot(n, h)), 64) * vec3(gl_LightSource[l_idx].specular);

        final_color += (spot * (diffuse_color + specular_color) + ambient_color / iLights) * attenuation(l_idx, light_dir);
    }

    FragColor = vec4(final_color, 1.);

}