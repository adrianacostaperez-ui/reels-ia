# Prueba de calidad de ojo — Blender / Cycles

Esta prueba sustituye el motor 3D de los vídeos anteriores. No se reutiliza
Three.js para generar las nuevas imágenes. Remotion solamente lee imágenes,
hace un acabado 2D muy suave y exporta el MP4. No hay texto ni pista de audio.

## Entorno comprobado

- El ejecutable del sistema es Blender 4.3.2 y sí ejecuta Cycles headless,
  pero su compilación no trae OpenImageDenoise integrado.
- Se instala Blender **5.2.2 LTS**, distribución oficial de Blender Foundation
  como módulo `bpy`, en `/workspace/blender-python` (Python 3.13).
- El render real usa **Cycles CPU**, cinco hilos, y OIDN integrado.
- No hay GPU disponible. `check_environment.py` hace un render real con
  Cycles/OIDN y escribe `out/blender-eye/environment.json`.
- La instalación local no modifica `/usr/bin/blender` ni requiere privilegios.
- `bpy` se obtuvo por PyPI con TLS y verificación normal de los paquetes.
  SHA-256 del wheel oficial Linux CPython 3.13 de bpy 5.2.2:
  `3dfd1a9e7a5aec0f0fe95a1b01d10cd66e212b16ea38b77d132159dc9a666d45`.

## Alcance de esta prueba y limitación importante

**El MP4 dura 5 segundos y tiene 150 fotogramas a 30 fps, pero no son
150 renders independientes de Cycles.**

Para este entorno de CPU se renderizan **31 posiciones reales de cámara**,
a resolución nativa de 1080 × 1920. Cada pose se renderiza con trazado de
caminos, hasta 24 muestras adaptativas, umbral .035, mínimo 8, y OIDN.
Después FFmpeg calcula los fotogramas intermedios con compensación de
movimiento; Remotion realiza el montaje 2D y la exportación final.

Esta optimización se comunica al usuario antes de ejecutarla. Sirve para
comparar materiales, iluminación, modelado y profundidad. No demuestra
el rendimiento ni la estabilidad temporal de una producción de 150 frames
nativos con más muestras. Para esa validación conviene una máquina con GPU
o una granja de render. La escena incluye los 150 frames de animación y
puede renderizarlos directamente en una instalación de Blender apropiada.

No se simula el acercamiento escalando una fotografía: los 31 originales
contienen parallax, reflejos y profundidad de campo de la cámara 3D.
La interpolación puede introducir pequeñas imprecisiones temporales;
se revisa el MP4 y se conserva la escena para pasar a render nativo después.

## Anatomía y materiales

- Globo escleral con espesor, dispersión subsuperficial y mapa de capilares.
- Iris curvo con más de 110000 vértices: estroma, criptas y margen pupilar.
- Mapas propios de color y relieve de 2048 px, generados de forma determinista.
- Córnea transparente separada, IOR 1.376, rugosidad .009 y reflejos físicos.
- Párpados con volumen, poros, variación de roughness y tejido húmedo.
- Pestañas curvas y cónicas, vello fino y carúncula lagrimal.
- Cierres de las superficies soldados para evitar costuras de normales
  visibles al fotografiar la córnea, el iris y la esclerótica en macro.
- Iluminación de estudio con áreas, key neutra y acentos azul/violeta;
  no se usa bloom ni emisión de neón para esconder detalle.
- Cámara macro de 100 mm, DOF real, enfoque en el iris y dolly de 5 segundos.
- AgX y viñeta 2D para el acabado de estudio oscuro.

Son materiales y geometría procedurales originales, no una captura anatómica
escaneada ni una fotografía proyectada. La prueba no implica que el nivel
publicitario de referencia ya esté aprobado: el usuario debe evaluar el MP4.

## Ejecutar en el entorno cloud

```sh
cd /workspace/reels-ia
bash blender/eye-quality/install.sh
bash blender/eye-quality/run.sh generate_textures
bash blender/eye-quality/run.sh create_scene --preview --scale 50 --samples 24 --frame 75
bash blender/eye-quality/run.sh render_frames
bash blender/eye-quality/run.sh interpolate
node scripts/render_blender_eye.mjs
bash blender/eye-quality/run.sh package_scene
bash blender/eye-quality/run.sh validate
```

`render_frames` reutiliza poses terminadas. Para cambiar modelo o iluminación,
quita únicamente las imágenes generadas de `out/blender-eye/anchors/` antes
de regenerarlas: no deben mezclarse renders de dos versiones.

La escena `.blend` empaquetada contiene texturas, materiales y cámara;
requiere Blender 5.2 compatible. Los renders y el informe de progreso quedan
en `out/blender-eye/`; las imágenes de montaje en `public/blender-eye/frames/`.
El archivo de entrega es `deliverables/blender-eye-quality-test.mp4`.

Para editar solamente el montaje, con las imágenes ya generadas:

```sh
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npx remotion studio src/blender-eye/index.tsx --port=3100 --no-open
```

Los atajos equivalentes son `npm run eye:studio`, `npm run eye:render` y
`npm run eye:check`. El montaje necesita primero las 150 imágenes generadas;
estas imágenes intermedias no se suben a Git. Sí se conserva la escena
empaquetada y el MP4, junto con las dependencias de Node fijadas en el lockfile.

Los vídeos y las escenas anteriores se conservan como historial. El nuevo
punto de entrada no importa Three.js ni React Three Fiber.
