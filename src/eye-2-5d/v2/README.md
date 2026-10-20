# Plano A — prueba 2.5D V2

Salida: deliverables/eye-2-5d-test-v2.mp4.
5 segundos, 1080 × 1920, 30 fps, 150 fotogramas, H.264, sin audio ni texto.

Parte de la misma imagen y de las mismas capas que la V1. El archivo original
y el primer MP4 se mantienen intactos. Se añade únicamente una máscara de foco
interior con los RGB originales: pupila e iris comparten exactamente la misma
transformación rígida y uniforme, sin deformación local ni cambios de anatomía.

## Diferencias de cámara

- Dolly más marcado, con aceleración gradual y avance adicional en el último
  tramo. La cámara sigue avanzando al terminar el plano, preparada para un corte
  de entrada a la pupila; no se detiene al final como en la V1.
- Recorrido lateral pequeño y reencuadre progresivo hacia la pupila, que termina
  aproximadamente en (552,952), cerca del centro del vídeo.
- Micro movimiento determinista de baja frecuencia, de amplitud inferior a un
  píxel, y roll máximo de 0,014 grados. Se reduce antes de la entrada final.
- Parallax algo mayor por profundidad entre piel, párpados/pestañas, córnea,
  iris y pase de reflexión; se mantienen márgenes y máscaras suaves.
- Foco primero sobre el iris y después sobre la pupila, con variación de campo
  de visión de como máximo 0,115 % para una respiración de lente muy contenida.
- El pase de reflexión tiene su propia profundidad y deriva sobre la córnea.
  Los reflejos ya fotografiados siguen en el original; esta técnica 2.5D no
  reconstruye una superficie 3D ni inventa el iris oculto bajo esos reflejos.

Los parámetros están en motion.ts. La imagen no se regenera. No se usa Blender,
Three.js, optical flow, inpainting, nuevas pestañas o geometría de ojo.

## Reproducir

    python scripts/prepare_eye_25d_v2.py
    npm run typecheck
    node scripts/render_eye_25d.mjs --v2 --stills
    node scripts/render_eye_25d.mjs --v2
    python scripts/validate_eye_25d.py --v2

Los fotogramas de revisión 0, 55, 105, 132 y 149 se guardan en
out/eye-2-5d-v2/. El último puede servir como referencia de continuidad para
el siguiente plano. La validación sigue la pupila en los 150 fotogramas,
comprueba la llegada al centro previsto, la conservación del original y de V1,
los RGB de todas las capas, formato, duración, ausencia de audio y decodificación.
