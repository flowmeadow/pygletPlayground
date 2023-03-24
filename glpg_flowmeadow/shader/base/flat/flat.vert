#version 130

uniform mat4 modelMatrix;

out vec2 uVec1;  // derivate vector for texturing without vertex seam
out vec2 uVec2;  // derivate vector for texturing without vertex seam
out vec3 fNormal;  // face normal
out vec3 fPosition;  // fragment position
out vec3 fColor;  // fragment color

void main ()
{
    // prepare derivative vectors for seamless texture wrapping
    // https://www.researchgate.net/publication/254311396_Cylindrical_and_Toroidal_Parameterizations_Without_Vertex_Seams
    vec2 uVecA = gl_MultiTexCoord0.st;
    uVec1 = fract(uVecA);
    uVec2 = fract(uVecA + 0.5) - 0.5;

    // compute position, color and face normal
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    fPosition = vec3(modelMatrix * gl_Vertex);
    fColor = vec3(gl_Color);
    fNormal = normalize(mat3(modelMatrix) * gl_Normal);
}