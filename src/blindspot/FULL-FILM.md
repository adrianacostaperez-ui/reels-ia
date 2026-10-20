# Punto ciego — versión completa V1

Salida: `deliverables/punto-ciego-v1.mp4`.
1080 × 1920, 30 fps, 1898 fotogramas (63,2667 s). La pista dura
63,245714 s; la diferencia es el redondeo de menos de un fotograma.

## Experimento bloqueado y aprobado físicamente

El usuario comprobó en su teléfono el experimento de `punto-ciego-test-15s.mp4`
y aprobó posiciones, tamaños, separación y fondo.

`config.ts` se conserva sin cambios. La versión completa importa `TestPlate`
directamente del test original; solamente se exporta esa función, sin alterar
su implementación. Cruz en x=190, punto en x=870; ambos en y=1030.
Cruz de 46 px y trazo de 6 px; punto de radio 15 px; fondo #05070b.
La prueba está fija desde el fotograma 58 hasta el 484 inclusive.

Se compararon PNG de resolución completa de las dos composiciones en los
fotogramas 165 y 390: diferencia máxima de cero píxeles en toda la imagen.
La pausa adicional ocupa los fotogramas 324–443 inclusive (10,8–14,8 s).
El texto permanece fijo hasta el inicio de la siguiente frase.

## Narración

Se usa el MP3 definitivo del usuario, sin TTS ni cambios de velocidad.
`prepare_blindspot_full.py` conserva todas las muestras decodificadas en
PCM de 24 bits, inserta exactamente 176400 muestras de silencio a 44100 Hz
en el segundo 10,8, y continúa desde esa misma muestra del audio original.
Comprueba igualdad exacta de las muestras anteriores y posteriores al empalme.
No hay música ni efectos superpuestos que dificulten la locución o la prueba.
El AAC de entrega se codifica a partir de ese PCM completo.

## Escenas y revisión

- 0–1,933 s: macro de ojo 3D con iris curvo, pupila abierta, córnea húmeda
  separada y reflejo de una pantalla; aproximación y luz azul/violeta.
- 1,933–16,167 s: experimento aprobado, estático. Desde 14,92 s continúa
  «El punto sigue ahí», conservando la lámina hasta la explicación.
- 16,167–21,81 s: proyección de la imagen hacia el fondo del ojo.
- 21,81–25,9 s: cámara atraviesa físicamente la pupila y llega a la retina.
- 25,9–30,41 s: ausencia de fotorreceptores y salida del nervio óptico.
- 30,41–32,61 s: vista externa de la salida y recorrido por el nervio.
- 32,61–41,41 s: punto ciego y luz que llega sin producir señal.
- 41,41–46,34 s: región sin información y cerebro esquemático.
- 46,34–50,34 s: comparación de pantalla y percepción; el fondo completa
  progresivamente la zona indicada, sin reconstruir el punto.
- 50,34–52,74 s: recordatorio con un solo ojo.
- 52,74–58,18 s: dos ojos 3D, campos visuales y compensación binocular.
- 58,18–final: regreso al ojo del hook. Movimiento termina con la voz;
  el resto de la cola original queda sostenido.

Modelos y materiales son procedurales. Los planos anatómicos son esquemas
tridimensionales: tamaños celulares y colores se simplifican para su lectura.
El disco óptico es tejido sin receptores, no un agujero físico en la retina.
Los rayos muestran tramos rectos con cambio de dirección en la lente.

Antes de renderizar el vídeo completo se generaron y revisaron fotogramas
de todas las escenas y las fases intermedias de entrada, relleno y cobertura.
Se corrigieron encuadres, la apertura de la pupila, la lectura del disco,
las etiquetas y las transiciones antes del render final.

## Reproducir en el entorno de trabajo

```sh
/workspace/voice-tools/bin/python scripts/prepare_blindspot_full.py
npm run typecheck
node scripts/review_blindspot_full.mjs
node scripts/render_blindspot_full.mjs
ffmpeg -v error -i out/blindspot-full/video-only.mp4 -i public/audio/punto-ciego-full.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -movflags +faststart deliverables/punto-ciego-v1.mp4
/workspace/voice-tools/bin/python scripts/validate_blindspot_full.py
```

Los informes de audio, imágenes y validación quedan en `out/blindspot-full/`.
La validación del MP4 examina ambos estímulos en los 427 fotogramas de
la prueba, los 120 fotogramas de la pausa y la narración completa; además
comprueba dimensiones, fps, duración y decodificación íntegra.

El informe de la entrega está en `validation-v1.json`. Además de la prueba,
se comprueba en un fotograma del vídeo secuencial que la región binocular
queda cubierta al completar la combinación. La pista AAC se conserva
paquete a paquete durante el ensamblado final.
