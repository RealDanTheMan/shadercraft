from __future__ import annotations
from uuid import UUID
import textwrap

from .asserts import assertRef, assertType, assertTrue
from .node import NodeValue
from .shadernodes import ShaderNodeIO, ShaderValueHint, ShaderNodeBase
from .vectors import Vec3F

class OutputShaderNodeBase(ShaderNodeBase):
    VertexShaderTarget: str = "template_standard.vs"
    PixelShaderTarget: str = "template_standard.ps"


class PhongOutputShaderNode(OutputShaderNodeBase):
    """
    Output shader node that supports Blinn-Phong lighting model.

    """
    VertexShaderTarget = "template_standard.vs"
    PixelShaderTarget = "template_standard.ps"
    label = "BlinnPhong"

    def __init__(self):
        super().__init__()
        self.name = "BlinnPhong Output Node"

        # Albedo node input
        self.albedo_input = ShaderNodeIO(
            "Albedo",
            "Albedo",
            ShaderValueHint.FLOAT3,
            static_value = Vec3F(1.0, 1.0, 1.0)
        )
        self._registerInput(self.albedo_input)

        # Alpha node input
        self.alpha_input = ShaderNodeIO(
            "Alpha",
            "Alpha",
            ShaderValueHint.FLOAT,
            static_value = 1.0
        )
        self._registerInput(self.alpha_input)

        # Normal node input
        self.normal_input = ShaderNodeIO(
            "Normal",
            "Normal",
            ShaderValueHint.FLOAT3,
            static_value = Vec3F(1.0, 1.0, 1.0)
        )
        self._registerInput(self.normal_input)

        # Specular node input
        self.spec_input = ShaderNodeIO(
            "Specular",
            "Specular",
            ShaderValueHint.FLOAT3,
            static_value = Vec3F(1.0, 1.0, 1.0)
        )
        self._registerInput(self.spec_input)

    def generateShaderCode(self) -> str:
        """
        Generate shader source code for this node.

        """

        albedo: NodeValue = self.getNodeInputValue(self.albedo_input.uuid)
        alpha: NodeValue = self.getNodeInputValue(self.alpha_input.uuid)
        normal: NodeValue = self.getNodeInputValue(self.normal_input.uuid)
        spec: NodeValue = self.getNodeInputValue(self.spec_input.uuid)

        assertRef(albedo)
        assertRef(alpha)
        assertRef(normal)
        assertRef(spec)

        src: str = f"""
        vec3 albedo = {albedo.value};
        float alpha = {alpha.value};
        vec3 normal = {normal.value};
        vec3 spec = {spec.value};
        """

        return textwrap.dedent(src).strip()
