#version 130


uniform vec3 cameraPos;  // camera position
uniform int iLights;  // number of light sources
uniform int iTime;  // number of textures
uniform sampler2D objTexture0;  // texture
uniform sampler2D objTexture1;  // texture

in vec3 fNormal;  // face normal
in vec3 fPosition;  // fragment position
in vec3 fColor;  // fragment color
in vec2 fTexCoord;

out vec4 FragColor;  // final fragment color

const vec2 grid_size = vec2(512., 512.);
const float grid_intensity = 0.2;


vec3 getNormal(vec2 uv, vec2 tex_size) {
    float step_x = 1. / grid_size.x;
    float step_y = 1. / grid_size.y;
    float h_x_min = texture2D(objTexture0, uv + step_x * vec2(-1.0, 0.0)).r;
    float h_x_max = texture2D(objTexture0, uv + step_x * vec2(1.0, 0.0)).r;
    float h_y_min = texture2D(objTexture0, uv + step_y * vec2(0.0, -1.0)).r;
    float h_y_max = texture2D(objTexture0, uv + step_y * vec2(0.0, 1.0)).r;

    vec3 h_x = vec3(2 * step_x, 0., abs(h_x_max - h_x_min));
    vec3 h_y = vec3(0., 2 * step_y, abs(h_y_max - h_y_min));

    vec3 n = cross(h_x, h_y);
    return normalize(n);
}


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
    vec2 tex_size = textureSize(objTexture0, 0);

    // compute view and normal vector
    vec3 v = normalize(cameraPos - fPosition);

    vec3 n = getNormal(fTexCoord, tex_size);
    vec3 xTangent = dFdx(fPosition);
    vec3 yTangent = dFdy(fPosition);
    n = normalize(cross(xTangent, yTangent));
//    n = fNormal;

    // compute texture color for the given position, using an approach for seamless texture wrapping
    // https://www.researchgate.net/publication/254311396_Cylindrical_and_Toroidal_Parameterizations_Without_Vertex_Seams

    vec3 texture_color = texture2D(objTexture1, fTexCoord).xyz;
//    texture_color = vec3(0.4, 0.4, 0.4);  // TODO

    // compute the current fragment's color, combining fragment and texture color
    vec3 object_color = fColor + texture_color;

    // color mesh black at pixel edges
    vec2 edge_width = vec2(1. / tex_size.x, 1. / tex_size.y);
    // Draw grid
    // TODO: Insanely ugly.

    vec2 dist = fTexCoord;
    dist.x -= edge_width.x * int(fTexCoord.x * tex_size.x);
    dist.y -= edge_width.y * int(fTexCoord.y * tex_size.y);
    float thresh = 5.0e-4;
    vec2 grid_err = abs(vec2(dist.x - edge_width.x, dist.y - edge_width.y));
    float grid_thickness = 5.0e-4;
    float x_fac = max(0., sign(grid_thickness - grid_err.x));
    float y_fac = max(0., sign(grid_thickness - grid_err.y));

    float val = min(1., x_fac + y_fac) * grid_intensity;
    //    while (dist.x > edge_width.x){
    //        dist.x -= edge_width.x;
    //    }
    //    while (dist.y > edge_width.y){
    //        dist.y -= edge_width.y;
    //    }

    vec3 grid_color = vec3(0., 0., 0.);

    //    if ((abs(dist.x - edge_width.x) < 0.0005) || (abs(dist.y - edge_width.y) < 0.0005)){
    //        object_color = grid_intensity * grid_color + (1. -grid_intensity) * object_color;
    //    }
    object_color = val * grid_color + (1. - val) * object_color;

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
        vec3 ambient_color  = 0.3  * (ambi_light_color * object_color);
        vec3 diffuse_color = 0.2 * max(0.0, dot(n, l)) * (diff_light_color * object_color);
        vec3 specular_color = 0.0 * pow(max(0.0, dot(n, h)), 10280) * (spec_light_color * object_color);

        // combine attenuation, spot and the computed colors to update the final fragment color
        final_color += (spot * (diffuse_color + specular_color) + ambient_color) * attenuation(l_idx, light_dir);
    }

    // return fragment color
    FragColor = vec4(final_color, 1.);
}