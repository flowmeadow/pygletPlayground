#version 130

out vec4 FragColor;

varying vec3 fcolor;

void main()
{
    FragColor = vec4(fcolor, 1.);
}