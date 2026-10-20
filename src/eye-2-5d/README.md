# Ojo original — prueba 2.5D de cinco segundos

Entrega: deliverables/eye-2-5d-test.mp4.
1080 × 1920, 30 fps, 150 fotogramas, H.264, sin texto ni audio.

La única imagen de partida es la PNG del ZIP suministrado por el usuario,
copiada sin modificar sus bytes a public/eye-2-5d/source.png.
SHA-256: 1767b8c9ed6cf6d40f4350c87813266ffcf5123fc7bb4a4a4385a04471a8c690.
Sus dimensiones son 941 × 1672; la salida se remuestrea a 1080 × 1920.
No se genera resolución o anatomía adicional.

## Construcción

- Piel, conjunto de párpados/pestañas, superficie ocular e iris: planos con
  máscaras alfa suaves obtenidos de los píxeles originales. Las pestañas
  conservan sus raíces y tejido adyacente en la misma capa.
- El iris y la pupila son una sola pieza rígida: cada plano tiene una escala
  uniforme y una traslación. No hay malla, morphing ni deformación local.
- Proyección por profundidad con avance suave de cámara, desplazamiento lateral
  y parallax pequeño para evitar bordes dobles entre capas.
- Cambio de foco suave hacia la pupila y desenfoque adicional en piel/pestañas.
- Un pase de luz óptica tenue se mueve sobre la córnea, recortado a su máscara.
  Los reflejos fotografiados originalmente siguen formando parte de la imagen;
  no se pretende reconstruir toda la óptica de un ojo desde una sola vista.
- Movimiento con continuidad de velocidad y aceleración en ambos extremos.
- Los 150 fotogramas se componen en Remotion, sin interpolación de vídeo.

Es animación 2.5D de una imagen: no es metraje de cámara ni vídeo generado por IA.
No usa Blender, Three.js, un ojo nuevo, pestañas sintetizadas, inpainting,
reconstrucción de zonas ocultas ni upscaling generativo.

## Reproducir

Desde /workspace/reels-ia, con Node y las dependencias del proyecto instalados:

    python scripts/prepare_eye_25d.py
    npm run typecheck
    node scripts/render_eye_25d.mjs --stills
    node scripts/render_eye_25d.mjs
    python scripts/validate_eye_25d.py

Preparación: Pillow y NumPy. Validación: SciPy y FFmpeg/ffprobe.
El entorno actual ya tiene estas dependencias y Chromium /usr/bin/chromium.
La validación compara todos los RGB de las capas contra la fuente, comprueba
el hash original y analiza continuidad/forma de la pupila en el MP4 completo,
además de duración, fps, resolución, ausencia de audio y decodificación.

Los parámetros de movimiento y profundidad están en config.ts. Los originales
de audio, el experimento aprobado y todos los vídeos anteriores se conservan.
