#version 130

uniform mat4 modelMatrix;
uniform sampler2D objTexture0;  // texture

out vec3 fNormal;  // face normal
out vec3 fPosition;  // fragment position
out vec3 fColor;  // fragment color
out vec2 fTexCoord;

vec3 getNormal(vec2 uv) {
    float step = 0.2;
    float h_y_min = texture2D(objTexture0, uv + step * vec2(0.0, -1.0)).r;
    float h_y_max = texture2D(objTexture0, uv + step * vec2(0.0, 1.0)).r;
    float h_x_min = texture2D(objTexture0, uv + step * vec2(-1.0, 0.0)).r;
    float h_x_max = texture2D(objTexture0, uv + step * vec2(1.0, 0.0)).r;

    vec3 h_x = vec3(2 * step, 0., abs(h_x_max - h_x_min));
    vec3 h_y = vec3(0., 2 * step, abs(h_y_max - h_y_min));

    vec3 n = cross(h_x, h_y);
    return normalize(n);
}


void main ()
{
    // compute position, color and face normal

    fTexCoord = gl_MultiTexCoord0.st;
    vec3 object_color = texture2D(objTexture0, fTexCoord).xyz;

    float height = gl_Vertex.z;
    if (gl_Vertex.z >= 0.)
        height = 0.25 * object_color.x;

    vec4 new_Vertex = vec4(gl_Vertex.x, gl_Vertex.y, height, 1);
//    new_Vertex = gl_Vertex;  // TODO

    gl_Position = gl_ModelViewProjectionMatrix * new_Vertex;
    fPosition = vec3(modelMatrix * new_Vertex);
    fColor = vec3(gl_Color);
    fNormal = normalize(mat3(modelMatrix) * gl_Normal);
//    fNormal = getNormal(fTexCoord);

}