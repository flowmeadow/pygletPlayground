vert_txt = """
#version 130

uniform mat4 modelMatrix;
uniform vec3 cameraPos;  // camera position
uniform int iLights;  // number of light sources
uniform int iTextures;  // number of textures
uniform sampler2D objTexture0;  // texture

out vec3 fColor;  // fragment color

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
    // compute view and normal vector
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    vec3 vPosition = vec3(modelMatrix * gl_Vertex);
    vec3 v = normalize(cameraPos - vPosition);
    vec3 n = normalize(mat3(modelMatrix) * gl_Normal);

    // compute texture color for the given position, using an approach for seamless texture wrapping
    vec2 uv_t = gl_MultiTexCoord0.st;
    vec3 texture_color = vec3(0., 0., 0.);
    texture_color += (iTextures > 0) ? texture2D(objTexture0, uv_t).xyz : vec3(0., 0., 0.);

    // compute the current fragment's color, combining fragment and texture color
    vec3 object_color = gl_Color.xyz + texture_color;

    // update the final fragment color for each light source individually
    vec3 final_color = vec3(0., 0., 0.);
    for (int l_idx = 0; l_idx < int(iLights); l_idx++){

        // compute light and half-way vector
        vec3 light_dir = vec3(gl_LightSource[l_idx].position) - vPosition;
        vec3 l = normalize(light_dir);
        vec3 h = (v + l) / length(v + l);

        // check if the current fragment is withon the light spot (1: True, 0: False)
        float spot = (1. - dot(-l, gl_LightSource[l_idx].spotDirection)) * 90.;
        spot = max(sign(gl_LightSource[l_idx].spotCutoff - spot), 0.);

        // compute ambient, diffuse and specular color
        vec3 ambi_light_color = vec3(gl_LightSource[l_idx].ambient);
        vec3 diff_light_color = vec3(gl_LightSource[l_idx].diffuse);
        vec3 spec_light_color = vec3(gl_LightSource[l_idx].specular);
        vec3 ambient_color  = 0.3  * (ambi_light_color * object_color);
        vec3 diffuse_color = 0.3 * max(0.0, dot(n, l)) * (diff_light_color * object_color);
        vec3 specular_color = 0.5 * pow(max(0.0, dot(n, h)), 256) * (spec_light_color * object_color);

        // combine attenuation, spot and the computed colors to update the final fragment color
        final_color += (spot * (diffuse_color + specular_color) + ambient_color) * attenuation(l_idx, light_dir);
    }

    // return vertex color
    fColor = final_color;
}
"""

frag_txt = """
#version 130

in vec3 fColor;  // fragment color

out vec4 FragColor;  // final fragment color


void main()
{
    FragColor = vec4(fColor, 1.);
}
"""