# Locución natural: preparada, pendiente de grabación

No se ha generado otra voz artificial. La locución de Kokoro usada en V3 no se reutiliza. Los MP4 anteriores permanecen intactos.

- `guion.txt`: texto exacto, sin instrucciones ni etiquetas que deban pronunciarse.
- `pista-reservada-8s.wav`: ocho segundos de **silencio**, reservados para la nueva locución. No es una voz ni un resultado final.
- `timing.json`: propuesta editorial para 1080×1920, 30 fps y ocho segundos. **Son tiempos orientativos, no medidos de una grabación.** Se reemplazan al recibir una toma natural.
- `peticion-tts.json`: petición preparada para ElevenLabs. No contiene claves ni un identificador de voz inventado.
- `conectar_elevenlabs.py`: conexión preparada con el endpoint oficial de voz y timestamps. Su integración de red está pendiente de probar con acceso real. `--check` valida la preparación sin gastar créditos ni enviar texto.

## Servicio recomendado

**ElevenLabs**, con una voz nativa española seleccionada después de escuchar una muestra de este guion. Como punto de partida, Eleven Multilingual v2 permite una lectura estable y obtener la alineación del texto. Un servicio o modelo no garantiza por sí solo que la voz elegida sea buena: hay que escuchar la toma antes de aprobarla. Una grabación humana con el mismo guion también sirve y puede sonar más cercana.

Conectar `ELEVENLABS_API_KEY` de forma segura en los ajustes del entorno, definir `ELEVENLABS_VOICE_ID` para la voz elegida y permitir `api.elevenlabs.io` en la red. No introducir claves en el chat ni en estos archivos.

```sh
python deliverables/narracion-natural/conectar_elevenlabs.py --check
# Solo cuando el servicio y una voz estén configurados:
python deliverables/narracion-natural/conectar_elevenlabs.py --generate
```

La generación es una toma candidata para escuchar, no una voz aprobada automáticamente. El script obtiene tiempos reales por palabra, prepara los subtítulos y los eventos del chip en `timing-alineado.json`, y guarda una pista candidata separada. El borrador no se sustituye hasta escuchar y aprobar la voz. Si no cabe de forma natural en ocho segundos, conserva la toma para revisión y **no la acelera, recorta ni actualiza el montaje**. La prioridad es la naturalidad.

## Dirección de interpretación

Una persona explicando una curiosidad a alguien cercano. Español neutro o de España nativo. Voz cálida, relajada y de registro medio, sin impostar graves ni sonreír como en un anuncio. Curiosidad suave en «no sabe exactamente»; primera frase casi como una confidencia. Pausa real de aproximadamente 250–350 ms tras «queda». «En realidad» debe sonar como una aclaración espontánea. Segunda frase tranquila, con intención en «chip» y «calcula», y caída suave al terminar. Evitar enumerar palabras, acentuar cada sílaba, terminar cada fragmento como una frase independiente o exagerar la sorpresa.

Grabar o sintetizar las dos frases completas de una vez. No separar la toma en fragmentos para generar los subtítulos. No modificar el texto hablado. No usar la voz de V3 ni procesamiento de tempo para intentar humanizarla.

## Montaje previsto

- 0,20–3,55 s: exterior del teléfono, tarjeta «1%», tres fragmentos de subtítulos.
- 3,92–4,52 s: «En realidad», breve transición en la interpretación.
- 4,64–5,43 s: «hay un chip», apertura y entrada al interior.
- 5,51–7,50 s: «que la calcula todo el tiempo», foco en el chip y pulsos.
- Final: pequeño margen de cierre.

El clic acompaña a la tarjeta; el whoosh a la entrada; la electricidad a los pulsos. Volver a alinear estos efectos con la toma real, manteniéndolos por debajo de la voz.

En Remotion Studio, `BatteryFilmNaturalVoiceDraft` permite revisar el guion y el montaje provisional **sin locución**; reutiliza el mismo modelo de V2/V3. No representa una nueva versión final del Reel.
