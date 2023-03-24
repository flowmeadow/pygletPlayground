#version 130


uniform vec3 cameraPos;  // camera position
uniform int iLights;  // number of light sources
uniform int iTime;  // number of textures
uniform sampler2D objTexture0;  // texture

in vec2 uVec1;  // derivate vector for texturing without vertex seam
in vec2 uVec2;  // derivate vector for texturing without vertex seam
in vec3 fNormal;  // face normal
in vec3 fPosition;  // fragment position
in vec3 fColor;  // fragment color

out vec4 FragColor;  // final fragment color


// computes light attenuation based on the distance to the light source and the source's attenuation parameter
float attenuation(int light_index, vec3 light_dir){
    float d = abs(length(light_dir));
    float attenuation = gl_LightSource[light_index].constantAttenuation;
    attenuation += gl_LightSource[light_index].linearAttenuation * d;
    attenuation += gl_LightSource[light_index].quadraticAttenuation * pow(d, 2);
    attenuation = 1. / attenuation;
    return attenuation;
}

float compute_cloud_val(vec2 tex_coord){
    float speed = 0.1 * 10e-6;
    vec2 tmp_1, tmp_2, tmp_3, tmp_4;
    tmp_1 = tmp_2 = tmp_3 = tmp_4 = tex_coord;
    tmp_1.x += 1.00 * (iTime + 1.23 * 10e3) * speed;
    tmp_2.x += 0.34 * (iTime + 2.34 * 10e4) * speed;
    tmp_3.x += 1.15 * (iTime + 3.45 * 10e5) * speed;
    tmp_4.x += 1.73 * (iTime + 4.56 * 10e6) * speed;

    float c_1 = texture2D(objTexture0, tmp_1).x;
    float c_2 = texture2D(objTexture0, tmp_2).x;
    float c_3 = texture2D(objTexture0, tmp_3).x;
    float c_4 = texture2D(objTexture0, tmp_4).x;
    float cloud_val = 1.2 * pow(sin(c_1 - c_4 + c_3 - c_2), 0.5);
    return cloud_val;
}


void main()
{
    // compute view and normal vector
    vec3 v = normalize(cameraPos - fPosition);
    vec3 n = normalize(fNormal);

    // compute texture color for the given position, using an approach for seamless texture wrapping
    // https://www.researchgate.net/publication/254311396_Cylindrical_and_Toroidal_Parameterizations_Without_Vertex_Seams
    vec2 uv_t;
    uv_t.x = (fwidth(uVec1.x) < fwidth(uVec2.x)-0.001) ? uVec1.x : uVec2.x;
    uv_t.y = (fwidth(uVec1.y) < fwidth(uVec2.y)-0.001) ? uVec1.y : uVec2.y;

    // compute cloud value
    vec3 texture_color = vec3(0.7, 0.75, 0.8);  // cloud color
    float cloud_val = compute_cloud_val(uv_t);
    cloud_val = max(dot(n, v), 0.) * cloud_val;

    // compute the current fragment's color, combining fragment and texture color
    vec3 object_color = fColor + texture_color;

    // update the final fragment color for each light source individually
    vec3 final_color = vec3(0., 0., 0.);
    for (int l_idx = 0; l_idx < int(iLights); l_idx++){

        // compute light and half-way vector
        vec3 light_dir = vec3(gl_LightSource[l_idx].position) - fPosition;
        vec3 l = normalize(light_dir);
        vec3 h = (v + l) / length(v + l);

        // check if the current fragment is withon the light spot (1: True, 0: False)
        float spot = (1. - dot(-l, gl_LightSource[l_idx].spotDirection)) * 90.;
        spot = max(sign(gl_LightSource[l_idx].spotCutoff - spot), 0.);

        // compute ambient, diffuse and specular color
        vec3 ambi_light_color = vec3(gl_LightSource[l_idx].ambient);
        vec3 diff_light_color = vec3(gl_LightSource[l_idx].diffuse);
        vec3 spec_light_color = vec3(gl_LightSource[l_idx].specular);
        vec3 ambient_color  = 0.1  * (ambi_light_color * object_color);
        vec3 diffuse_color = 0.5 * max(0.0, dot(n, l)) * (diff_light_color * object_color);
        vec3 specular_color = 0.5 * pow(max(0.0, dot(n, h)), 16) * (spec_light_color * object_color);

        // combine attenuation, spot and the computed colors to update the final fragment color
        final_color += (spot * (diffuse_color + specular_color) + ambient_color) * attenuation(l_idx, light_dir);
    }

    // return fragment color
    FragColor = vec4(final_color, cloud_val);
}