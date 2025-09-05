# Open Paths (CC→FE)

**Scope permitido**: contribuciones en niveles **CC/CI/CP/FE** dentro de cada
componente `CE-*` (p. ej., `.../CE-CAD-Q100-AAA-ATA-56-.../CC/**`, `CI/**`,
`CP/**`, `FE/**`).

**Prohibido**:
- Cambios en **CE** o rutas por encima de CC (docs de sistema, compliance a nivel CE).
- Cambios en **QS/**.
- Cambios en `.github/**`, workflows o configuraciones (salvo por maintainers).
- Cambios en S1000D DMs salvo instrucción explícita (gobernanza CAS).

**Cómo participar**:
1. Abre un PR desde fork con la etiqueta `open-collab:cc-fe`.
2. Coloca los artefactos dentro de `CC/`, `CI/`, `CP/` o `FE/` bajo el CE correspondiente.
3. Incluye enlaces a EBOM/MBOM/RTM si aplica, y respeta `yamllint`.

**Revisión**:
- CODEOWNERS exige revisión de `@best-contributor` y del equipo mantenedor.