#version 130

in vec3 fColor;  // fragment color

out vec4 FragColor;  // final fragment color


void main()
{
    FragColor = vec4(fColor, 1.);
}