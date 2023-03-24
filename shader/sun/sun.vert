#version 130

uniform mat4 modelMatrix;

out vec3 fNormal;  // face normal
out vec3 fPosition;  // fragment position

void main ()
{
    // compute position, color and face normal
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    fPosition = vec3(modelMatrix * gl_Vertex);
    fNormal = normalize(mat3(modelMatrix) * gl_Normal);
}