# Punto ciego — prueba de 15 segundos

Únicamente hook y experimento. No contiene retina, nervio ni cerebro.
1080 × 1920, 30 fps, 450 fotogramas.

## Ajustar para la prueba física

Editar `config.ts`. `fixationX` es la cruz; el punto está en
`fixationX + separationPx`. Ambos usan `stimulusY`. La separación inicial
es 680 px; no hay animaciones de posición, tamaño, cámara o fondo desde
el fotograma 58 (1,933 s). El texto de pausa aparece fijo en el 324
(10,8 s) y permanece hasta el final.

Mostrar a pantalla completa en vertical, cerrar el ojo izquierdo,
fijar la cruz izquierda con el derecho y mover lentamente el teléfono.
En una pantalla de unos 6,5 cm de ancho, la separación corresponde a
unos 4,1 cm; una distancia de observación aproximada de 15 cm la sitúa
alrededor de 15 grados a la derecha de la fijación. La prueba real en
el dispositivo sigue pendiente: depende de su tamaño físico y del espectador.
El punto permanece dibujado en todos los fotogramas.

## Audio

MP3 definitivo del usuario, SHA-256:
`05e542237413c0c80517bca585b8b844563d38141935eb19dd34d4d620f23053`.
Se conservan las muestras de 0 a 10,8 s sin cambios de ritmo o volumen.
Se añaden 4 s de silencio y se mantiene la placa hasta los 15 s.
La frase «El punto sigue ahí», que entraría en 14,92 s, se reserva
completa para el vídeo largo; no se corta su primera palabra en esta prueba.
No hay TTS ni efectos superpuestos. El original queda intacto.

## Producir esta prueba en el entorno existente

```sh
/workspace/voice-tools/bin/python scripts/prepare_blindspot_test.py
npm run typecheck
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium npx remotion render src/blindspot/index.tsx BlindSpotTest15s out/blindspot/video-only.mp4 --crf=16 --pixel-format=yuv420p --muted
ffmpeg -v error -i out/blindspot/video-only.mp4 -i public/audio/punto-ciego-test-15s.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -t 15 -movflags +faststart deliverables/punto-ciego-test-15s.mp4
/workspace/voice-tools/bin/python scripts/validate_blindspot_test.py
```

Las comprobaciones analizan los dos estímulos en los 392 fotogramas
del experimento y toda la imagen durante la pausa, además del audio.
No sustituyen la comprobación perceptiva en un teléfono real.
