// Standard template for generated vertex shader

#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in vec3 normal;

uniform mat4 sv_view;
uniform mat4 sv_model;
uniform mat4 sv_perspective;

out vec3 pix_position;
out vec3 pix_color;
out vec3 pix_normal;

void main() {
	//mat4 mvp = sv_model * sv_view * sv_perspective;
	mat4 mvp = sv_perspective * sv_view * sv_model;
	vec4 vpos = mvp * vec4(position, 1.0f);

	pix_position = vpos.xyz;
	pix_color = color;
	pix_normal = normal;

	gl_Position = vpos;
}
