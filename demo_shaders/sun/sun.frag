#version 130


uniform vec3 cameraPos;  // camera position

in vec3 fNormal;  // face normal
in vec3 fPosition;  // fragment position

out vec4 FragColor;  // final fragment color


void main()
{
    // compute view and normal vector
    vec3 v = normalize(cameraPos - fPosition);
    vec3 n = normalize(fNormal);

    // compute light parameter
    vec3 light_color = vec3(gl_LightSource[0].ambient);
    float l_1 = pow(dot(n, v), 7.);
    float l_2 = pow(dot(n, v), 3.);

    // return fragment color
    FragColor = vec4(l_1 * light_color, l_2);
}