#version 130


uniform sampler2D objTexture0;  // texture

in vec2 uVec1;  // derivate vector for texturing without vertex seam
in vec2 uVec2;  // derivate vector for texturing without vertex seam
in vec3 fNormal;  // face normal
in vec3 fPosition;  // fragment position
in vec3 fColor;  // fragment color

out vec4 FragColor;  // final fragment color


void main()
{
    // compute texture color for the given position, using an approach for seamless texture wrapping
    // https://www.researchgate.net/publication/254311396_Cylindrical_and_Toroidal_Parameterizations_Without_Vertex_Seams
    vec2 uv_t;
    uv_t.x = (fwidth(uVec1.x) < fwidth(uVec2.x)-0.001) ? uVec1.x : uVec2.x;
    uv_t.y = (fwidth(uVec1.y) < fwidth(uVec2.y)-0.001) ? uVec1.y : uVec2.y;

    vec3 texture_color = texture2D(objTexture0, uv_t).xyz;  // cloud color
    float lightness = 0.3 * (texture_color.x + texture_color.y + texture_color.z);
    lightness = pow(lightness, 2);

    // return fragment color
    FragColor = vec4(lightness * texture_color, 1.);
}