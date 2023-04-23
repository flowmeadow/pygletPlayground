#version 130


uniform vec3 cameraPos;  // camera position
uniform int iLights;  // number of light sources
uniform int iTime;  // number of textures
uniform sampler2D objTexture0;  // texture
uniform sampler2D objTexture1;  // water map
uniform sampler2D objTexture2;  // height map
uniform sampler2D objTexture3;  // night lights

in vec2 uVec1;  // derivate vector for texturing without vertex seam
in vec2 uVec2;  // derivate vector for texturing without vertex seam
in vec3 fNormal;  // face normal
in vec3 fPosition;  // fragment position
in vec3 fColor;  // fragment color

out vec4 FragColor;  // final fragment color

#define M_PI 3.1415926535897932384626433832795

// computes light attenuation based on the distance to the light source and the source's attenuation parameter
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
    // helper variables
    float step;
    vec2 step_x, step_y;

    // compute view and normal vector
    vec3 v = normalize(cameraPos - fPosition);
    vec3 n = normalize(fNormal);

    // compute texture color for the given position, using an approach for seamless texture wrapping
    // https://www.researchgate.net/publication/254311396_Cylindrical_and_Toroidal_Parameterizations_Without_Vertex_Seams
    vec2 uv_t;
    uv_t.x = (fwidth(uVec1.x) < fwidth(uVec2.x)-0.001) ? uVec1.x : uVec2.x;
    uv_t.y = (fwidth(uVec1.y) < fwidth(uVec2.y)-0.001) ? uVec1.y : uVec2.y;
    vec3 texture_color = texture2D(objTexture0, uv_t).xyz;

    // get normal from height map
    step = 0.1 * 10e-4;
    step_x = vec2(step, 0.);
    step_y = vec2(0., step);
    float h_x = texture2D(objTexture2, uv_t + step_x).x - texture2D(objTexture2, uv_t - step_x).x;
    float h_y = texture2D(objTexture2, uv_t + step_y).x - texture2D(objTexture2, uv_t - step_y).x;

    // apply normal
    vec3 n_rad = cross(n, vec3(0., 0., 1.));
    vec3 n_tan = cross(n, n_rad);
    n = n + 10. * (n_rad * h_x - n_tan * h_y);  // 0.8
    n = normalize(n);

    // get water value
    float water = texture2D(objTexture1, uv_t).x;

    // identify coast region
    step = 0.0005 * (sin(iTime * 10e-4 + pow(uv_t.y * 0.1, 1.) * uv_t.x * 5. * 10e2) + 2.);
    step_x = vec2(step, 0.);
    step_y = vec2(0., step);
    float c_x = texture2D(objTexture1, uv_t + step_x).x - texture2D(objTexture1, uv_t - step_x).x;
    float c_y = texture2D(objTexture1, uv_t + step_y).x - texture2D(objTexture1, uv_t - step_y).x;
    float coast = min(abs(c_x) + abs(c_y), 1.);

    // wave effect
    vec3 wave_color = 0.5 * texture_color + 0.5 * vec3(1., 1., 1.);
    wave_color = water * wave_color + (1. - water) * texture_color;
    texture_color = coast * wave_color + (1. - coast) * texture_color;

    // update texture at night (only land)
    vec3 light_dir = vec3(gl_LightSource[0].position) - fPosition;
    vec3 l = normalize(light_dir);
    float night = (1. - water) * (1. - max(0.0, dot(n, l)));
    night = 0.7 * pow(night, 8.);
    vec3 night_color = texture2D(objTexture3, uv_t).xyz;
    float night_light = (night_color.x + night_color.y + night_color.z) / 3.;
    texture_color = night * night_color + (1. - night) * texture_color;

    // compute the current fragment's color, combining fragment and texture color
    vec3 object_color = fColor + texture_color;

    // update the final fragment color for each light source individually
    vec3 final_color = vec3(0., 0., 0.);
    for (int l_idx = 0; l_idx < int(iLights); l_idx++){

        // compute light and half-way vector
        light_dir = vec3(gl_LightSource[l_idx].position) - fPosition;
        l = normalize(light_dir);
        vec3 h = (v + l) / length(v + l);

        // check if the current fragment is withon the light spot (1: True, 0: False)
        float spot = (1. - dot(-l, gl_LightSource[l_idx].spotDirection)) * 90.;
        spot = max(sign(gl_LightSource[l_idx].spotCutoff - spot), 0.);

        // compute ambient, diffuse and specular color
        vec3 ambi_light_color = vec3(gl_LightSource[l_idx].ambient);
        vec3 diff_light_color = vec3(gl_LightSource[l_idx].diffuse);
        vec3 spec_light_color = vec3(gl_LightSource[l_idx].specular);

        float amb_a = (1. - night) * 0.1 + night * night_light;
        float spec_a = 0.1 + water * 0.3;
        float spec_b = 16 + water * 256;


        vec3 ambient_color  = amb_a  * (ambi_light_color * object_color);
        vec3 diffuse_color = 0.5 * max(0.0, dot(n, l)) * (diff_light_color * object_color);
        vec3 specular_color = spec_a * pow(max(0.0, dot(n, h)), spec_b) * (spec_light_color);

        // combine attenuation, spot and the computed colors to update the final fragment color
        final_color += (spot * (diffuse_color + specular_color) + ambient_color) * attenuation(l_idx, light_dir);
    }
    // return fragment color
    FragColor = vec4(final_color, 1.);
}