# Punto ciego — storyboard para visuales generados por IA

Estado: plano A aprobado como recurso 2.5D; el resto es una propuesta de producción.
La regla de montaje actual está en src/blindspot/ai-edit-policy.json.

## Selección aprobada y ritmo de montaje

- A es deliverables/eye-2-5d-test-v2.mp4. Usar sólo sus primeros 58 frames
  ([0,58), 1,9333 s), a velocidad original, al principio del vídeo.
- Conservar el master de cinco segundos. Su cola no se emplea para extender A
  ni para rellenar un inserto posterior. No generar una V3.
- Recursos 2.5D preferiblemente de 1,5–2,5 s, con un máximo continuo de 3 s.
  Alternar imágenes distintas, detalles, recortes, overlays explicativos y
  transiciones con función narrativa. Varios recortes consecutivos de una
  misma foto no deben convertirse en otra forma de prolongarla artificialmente.
- El experimento aprobado es la excepción: conserva sus estímulos y fondo
  inmóviles, su duración y la pausa de cuatro segundos, sin introducir cortes.
- Los bloques narrativos y los prompts del resto del documento conservan el
  guion y la intención visual. Los intervalos largos se subdividen en planos
  cortos antes del montaje; no autorizan sostener una sola imagen todo el bloque.
- La referencia de continuidad desde el A seleccionado es el frame 57, no el
  final de cinco segundos del test. Los recursos B/I posteriores deben aportar
  imágenes o movimiento propios, en lugar de estirar A.

## Base que se conserva

- Guion y cues de src/blindspot/approved-timeline.json.
- MP3 definitivo: public/audio/punto-ciego-narracion-original.mp3. La pista derivada aprobada public/audio/punto-ciego-full.wav ya contiene la pausa; no se vuelve a insertarla.
- Duración narrativa: 63,245688 s, presentada como 63,25 s. La exportación existente a 30 fps usa 1898 fotogramas, 63,2667 s, por el redondeo final; se conserva ese criterio.
- Subtítulos aprobados, con sus fragmentos, tiempos y estilo V6: captions.ts y full-captions.ts. Mismo tratamiento superior y una sola palabra destacada por fragmento.
- Lámina experimental: cruz (190,1030), punto (870,1030), cruz de 46 px y trazo de 6 px, radio del punto 15 px, separación 680 px; fondo #05070b; estímulos #f0f3fa. La lámina permanece inmóvil en los frames 58–484 inclusive.
- Pausa adicional: 10,80–14,80 s, frames 324–443 inclusive. Se conserva el texto fijo «Puedes pausar para probar» y su margen de salida ya aprobado. Sin movimientos, efectos, música ni animaciones durante la pausa.

## Dirección de arte y continuidad

Ojo derecho de una misma persona adulta ficticia; iris azul grisáceo con corona ámbar muy discreta. Piel, vasos y tejidos mantienen colores naturales. Negros profundos, luz principal blanca suave desde arriba a la izquierda, acento azul del mismo lado y recorte violeta suave desde la derecha. El iris, la forma de los párpados y el reflejo rectangular de pantalla se fijan en una imagen maestra; A, B, H e I deben usarla como referencia visual.

La cámara avanza de fuera hacia dentro, con desplazamiento lateral leve hacia la derecha del encuadre, sin roll, espejado horizontal ni órbitas que inviertan el eje. Los interiores mantienen ese sentido de avance. D, E y F comparten referencias anatómicas y posición coherente del disco óptico respecto de la fóvea. La luz azul/violeta es un acento de iluminación, no el color de los tejidos.

El cambio de retina completa a células microscópicas es un cambio de escala mediante corte; no se muestran fotorreceptores brotando de la cara interna de la retina. El disco óptico es tejido sin fotorreceptores, no un agujero negro ni una lesión. La proyección del campo temporal del ojo derecho debe llegar a retina nasal. Estas relaciones se revisan contra referencias anatómicas antes de aceptar las imágenes.

Los prompts piden imágenes limpias, sin textos ni símbolos. La proyección del punto, la ausencia de señal, el relleno y la compensación binocular se controlan en composición 2D. El relleno es una representación explicativa, no una grabación literal del funcionamiento cerebral.

Exclusiones comunes para todos los prompts: texto, subtítulos incrustados, letras, logos, marcas de agua, HUD, dashboards, diagramas decorativos, ojos adicionales, iris duplicados, pupilas deformadas, anatomía mutante, tejidos que cambian de forma, aspecto plástico, low-poly, exceso de glow, láseres, túneles de ciencia ficción, galaxias dentro del ojo, gore y movimientos de cámara erráticos.

## Storyboard y timeline

Los segundos de la tabla reproducen los cues narrativos. En montaje se mantienen los límites en fotogramas de la versión aprobada. Las filas describen bloques narrativos; cuando exceden 2–3 s se subdividen con cambios de plano reales, imágenes distintas y composición 2D, según la regla superior.

| Tiempo | Duración | Asset / escena | Acción y relación con la voz |
|---|---:|---|---|
| 0,00–1,94 | 58 frames, 1,9333 s | A aprobado | Primeros 58 frames de eye-2-5d-test-v2.mp4: «Tu ojo no ve toda esta pantalla». Corte directo al experimento. |
| 1,94–10,80 | 8,86 s | EXP, 2D aprobada | Instrucciones originales. Cruz a izquierda y punto a derecha; nada cambia de posición, tamaño o fondo. |
| 10,80–14,80 | 4,00 s | EXP, 2D aprobada | Pausa completamente estática con «Puedes pausar para probar». |
| 14,80–16,16 | 1,36 s | EXP, 2D aprobada | Continúa la misma lámina; «El punto sigue ahí» entra en su cue de 14,92 s. |
| 16,16–19,32 | 3,16 s | B | Regreso al mismo ojo y avance hacia la pupila: «Pero, a esa distancia, su imagen cae justo…». |
| 19,32–21,81 | 2,49 s | F, primera aparición | Corte anatómico del ojo. Sobre la imagen se anticipa en 2D la zona donde llega la proyección. |
| 21,81–22,76 | 0,95 s | C | «Mira adentro»: entrada rápida por la pupila; corte oculto en su oscuridad y llegada al interior. |
| 22,76–23,78 | 1,02 s | D1 | Retina cóncava y vascularizada: «Al fondo está la retina». |
| 23,78–25,90 | 2,12 s | D2 | Corte de escala a una sección microscópica: células que detectan luz. |
| 25,90–28,43 | 2,53 s | E1, detalle | La capa de fotorreceptores termina en el disco óptico: «…donde no hay ninguna». |
| 28,43–30,41 | 1,98 s | E1, apertura de encuadre | El mismo corte permite reconocer la salida del nervio, sin transformar tejido ni abrir un agujero. |
| 30,41–32,61 | 2,20 s | E2 | Recorrido corto por el nervio hacia el cerebro. Señal ilustrativa tenue añadida en 2D. |
| 32,61–35,22 | 2,61 s | F, plano general | Ubicación del punto ciego en el disco óptico, separada de la fóvea. |
| 35,22–38,38 | 3,16 s | F, detalle | Proyección del punto sobre el disco; no aparece respuesta saliente. Los elementos explicativos se animan en Remotion. |
| 38,38–41,41 | 3,03 s | F, reencuadre | Relación entre el punto exterior, que sigue presente, y la zona sin detección. |
| 41,41–43,14 | 1,73 s | PER, composición 2D | «¿Y por qué no ves un hueco negro?»: campo perceptivo continuo, sin dibujar un agujero físico en el ojo. |
| 43,14–46,34 | 3,20 s | G | Macro del córtex occipital; avance 2.5D mínimo mientras se explica el papel del cerebro. |
| 46,34–48,10 | 1,76 s | PER, composición 2D | Comparación explicativa de estímulo y percepción: el entorno aporta el fondo. |
| 48,10–50,34 | 2,24 s | PER, composición 2D | El fondo queda continuo y el punto no se reconstruye. Es una simulación posterior al experimento, identificada como tal. |
| 50,34–52,74 | 2,40 s | J, inserto alternativo pendiente | Otra imagen del mismo ojo abierto para «Incluso con un solo ojo abierto»; no reutilizar la cola de A ni alargar el recurso aprobado. |
| 52,74–54,93 | 2,19 s | H, primera parte | Ambos ojos de la misma persona; se abre el izquierdo. |
| 54,93–58,18 | 3,25 s | H, segunda parte | Compensación del otro ojo. Máscaras 2D muestran regiones faltantes distintas y la información combinada. |
| 58,18–60,65 | 2,47 s | I, primera parte | Vuelta al ojo derecho: «Así que no ves el mundo exactamente como es». |
| 60,65–63,25 | ≈2,60 s | I, segunda parte | Último avance y ajuste de foco; el movimiento concluye con la última palabra y conserva la cola original del audio. |

## Banco de recursos y selección actual

A ya existe y está aprobado. El resto son familias visuales propuestas; el número definitivo de imágenes se amplía donde hagan falta alternativas para mantener planos cortos. EXP y PER se realizan en Remotion y no requieren generación por IA. Los tiempos de la tabla son asignaciones narrativas totales, no duración continua de una imagen.

| ID | Recurso | Fuente solicitada | Uso total en montaje |
|---|---|---|---:|
| A | Macro exterior aprobado | Recurso 2.5D V2 existente, master de 5 s | Sólo 1,9333 s iniciales, una aparición |
| B | Aproximación a la pupila | Vídeo, master de 5 s | 3,16 s |
| C | Entrada al interior | Vídeo, master de 5 s | 0,95 s |
| D1 | Retina completa desde el vítreo | Imagen vertical de alta resolución | 1,02 s |
| D2 | Sección microscópica de retina | Imagen vertical de alta resolución | 2,12 s |
| E1 | Disco óptico y salida del nervio en sección | Imagen vertical de alta resolución | 4,51 s |
| E2 | Trayecto del nervio | Vídeo, master de 5 s | 2,20 s |
| F | Ojo derecho en corte anatómico | Imagen vertical de alta resolución | 11,29 s, repartidos en cuatro apariciones/reencuadres |
| G | Córtex occipital | Imagen vertical de alta resolución | 3,20 s |
| H | Visión binocular, mismo rostro | Vídeo, master de 8 s | 5,44 s |
| I | Macro final del mismo ojo | Vídeo, master de 8 s | ≈5,07 s |
| J | Inserto alternativo del ojo abierto | Imagen distinta pendiente | 2,40 s; sin reutilizar la cola de A |

Los masters de 5/8 s son solicitudes de trabajo; si el servicio ofrece otras duraciones, se elige la suficiente y se recorta. No se cambia la voz para ajustarla a un clip. Para las imágenes, 2.5D significa recortes, capas y desplazamientos pequeños; no órbitas falsas ni síntesis de superficies que la imagen no muestra.

## Prompts completos

### A — Macro cinematográfico del ojo

No requiere nueva generación. Usar el recurso aprobado eye-2-5d-test-v2.mp4,
frames 0–57 inclusive, a 30 fps y velocidad 1×. Mantener la imagen y el movimiento
existentes; sin bucles, congelados, ralentización o V3. Cortar al experimento
en el frame 58. El plano aprobado sirve como referencia de identidad y acabado
para las demás imágenes del ojo, sin prolongarlo artificialmente.

### B — Acercamiento a la pupila

Generar vídeo vertical 9:16, master de 5 segundos, del que se usarán 3,16 segundos. Usar el ojo derecho y la identidad del plano A como referencia, conservando iris, párpados, vasos y reflejo de pantalla. Composición frontal con oblicuidad mínima, pupila cerca del centro inferior a la zona reservada para subtítulos. Lente macro de 100–120 mm, f/5.6 equivalente; foco continuo sobre el margen pupilar y ligera pérdida de foco hacia los párpados. Dolly físico hacia delante con deriva mínima a la derecha; la pupila aumenta por la cámara, sin dilatarse ni cambiar de forma. Córnea húmeda y refractiva, piel con microtextura y esclerótica orgánica, realismo publicitario. Mantener key blanca arriba-izquierda, azul izquierdo, violeta derecho y negros profundos de A. El plano retoma A después de la prueba estática; su último fotograma será referencia de entrada para C. Entre ambos se intercala el corte explicativo F, conectado por forma y dirección. Sin túneles, reflejos independientes de la cámara, deformaciones ni texto.

### C — Viaje visual hacia el interior

Generar vídeo vertical 9:16, master de 5 segundos, con una entrada rápida utilizable de aproximadamente 0,95 segundos. Partir del margen pupilar del último fotograma de B, con el mismo ojo, eje y reflejos. Lente macro equivalente de 120 mm que pasa a una óptica virtual amplia de 24–35 mm al entrar; avance exclusivamente hacia delante, sin roll ni inversión de dirección. La córnea y el cristalino son medios transparentes, no un túnel de tejido. Usar una breve oclusión oscura dentro de la pupila como punto de empalme y revelar al final la cavidad vítrea con la retina curva al fondo, compatible con D1. Iluminación motivada por la abertura anterior y acentos fríos discretos; tejido con color natural, humedad moderada, sin neón ni partículas flotantes decorativas. Profundidad de campo pasa de muy corta a suficiente para reconocer la pared retinal. Reconstrucción anatómica cinematográfica plausible, no una endoscopia literal ni una travesía por galaxias. Sin morphing de iris en retina y sin fotorreceptores gigantes en el vítreo.

### D1 — Retina vista desde el interior

Generar una imagen vertical 9:16 de alta resolución para un plano de 1,02 segundos. Vista anatómica cinematográfica de la pared interna cóncava de la retina del ojo derecho, observada desde el vítreo. Retina rosado rojiza natural, superficie húmeda de brillo muy sutil y vasos ramificados orgánicos; disco óptico en retina nasal y fóvea claramente separados, con ubicación fijada por referencia anatómica. Composición llena, sin globo aislado flotando; dejar el área superior poco contrastada para subtítulos. Óptica virtual de 35–50 mm, profundidad de campo moderada, suficiente para leer curvatura y relieve. Luz suave anterior, sombras profundas y acentos azul/violeta coherentes con C, sin convertir el tejido en material azul. Realismo de reconstrucción médica de alta gama. La imagen será el destino del viaje C y permitirá un avance 2D mínimo. El corte siguiente D2 cambia explícitamente de escala hacia una sección microscópica. No mostrar conos y bastones expuestos sobre la cara vítrea, letras ni flechas incrustadas.

### D2 — Fotorreceptores a escala microscópica

Generar imagen vertical 9:16 de alta resolución para una inserción de 2,12 segundos. Reconstrucción médica microscópica verosímil de una sección de retina: capas coherentes y capa externa de fotorreceptores, con conos y bastones diferenciados y relación espacial correcta con el epitelio pigmentario. Composición oblicua y cercana que llena el encuadre, destacando un grupo de células sin convertirlas en cilindros uniformes ni en vegetación. Materiales biológicos translúcidos, membranas finas e irregularidad orgánica; colores naturales gris rosado, iluminación blanca suave arriba-izquierda y recorte azul/violeta muy contenido. Óptica de microscopía equivalente a objetivo 40×, foco selectivo sobre los segmentos externos, profundidad de campo corta con suficiente lectura de capas. No se presenta como fotografía clínica real, sino como reconstrucción científica cinematográfica. Remotion hará un desplazamiento mínimo, sin inventar rotaciones. Entrada desde D1 mediante corte de escala; salida a E1 conservando orientación de capas y mostrando después dónde dejan de existir esos receptores. Sin impulsos mágicos ni texto generado.

### E1 — Disco óptico y salida del nervio

Generar imagen vertical 9:16 de alta resolución para dos encuadres consecutivos que suman 4,51 segundos. Sección anatómica detallada del ojo derecho centrada en el disco óptico nasal y la salida posterior del nervio; mostrar cómo las capas de fotorreceptores presentes en retina adyacente terminan antes del disco, mientras los axones convergen y salen hacia atrás. El disco es tejido pálido vivo, no un hueco negro, una herida ni la fóvea. Conservar posición y dirección acordadas con D1/D2 y con el corte general F. Material biológico húmedo pero no gelatinoso, vasos finos naturales, envolturas y transición de tejido plausibles. Lente virtual de 70–90 mm, profundidad de campo moderada para reconocer el vínculo entre retina y nervio. Luz blanca suave superior izquierda, azul y violeta sólo como recortes, fondo oscuro y tejidos de color natural. Realismo de ilustración médica cinematográfica de alta gama. Un recorte empieza sobre la ausencia de receptores y otro revela la salida completa, mediante movimiento 2D suave. E2 continúa por ese nervio en el mismo sentido. Sin geometría simplificada ni anotaciones incrustadas.

### E2 — Recorrido por el nervio óptico

Generar vídeo vertical 9:16, master de 5 segundos, con 2,20 segundos útiles. Partir de la salida posterior del nervio mostrada en E1 y seguir un tramo corto hacia el cerebro, manteniendo el mismo sentido de avance y una deriva lateral mínima. Encuadre macro oblicuo lleno de tejido, sin nervio aislado flotando en un vacío. Reconstrucción anatómica detallada de haces y envolturas, con superficie fibrosa húmeda y color marfil rosado apagado; no cables, cristal ni tubos luminosos. Óptica virtual de 60–85 mm y profundidad de campo corta, con foco que acompaña el tramo visible. Key blanca superior izquierda, azul de borde a izquierda y violeta suave a derecha, contraste oscuro coherente con E1. La anatomía permanece estable, sin aparición de ramas ni fibras que se fundan entre fotogramas. No generar señales eléctricas: una indicación de propagación tenue se añadirá después en 2D como recurso explicativo. Terminar estable para cortar a la localización general del punto ciego en F. Sin HUD ni texto.

### F — Representación anatómica del punto ciego

Generar imagen vertical 9:16 de alta resolución para cuatro apariciones que suman 11,29 segundos, con distintos recortes y composición 2D. Ojo derecho humano en corte anatómico sagital-oblicuo que permita reconocer córnea, cristalino, vítreo, retina, fóvea y disco óptico nasal sin solaparlos. Mostrar una porción realista de órbita y tejido alrededor para dar volumen, sin esfera flotante ni diagrama de círculos. Dejar espacio útil para incorporar después un pequeño estímulo exterior y una proyección óptica físicamente coherente desde campo temporal hacia retina nasal. No generar el punto, rayos, señales ni etiquetas: Remotion los colocará con precisión. Lente virtual de 65 mm, profundidad de campo suficiente para mantener legible el recorrido óptico; materiales orgánicos con humedad y rugosidades distintas, sin transparencia de plástico. Luz principal blanca arriba-izquierda, acentos azul/violeta discretos y fondo oscuro. Compartir anatomía y posición del disco con D1/E1. Primera aparición entre B y C; después se reutiliza tras E2 para localizar el punto ciego y explicar la ausencia de señal. Realismo médico cinematográfico, sin lesión ni agujero físico en el disco.

### G — Cerebro y completado perceptivo

Generar imagen vertical 9:16 de alta resolución para un plano de 3,20 segundos. Macro anatómico de la región occipital de un cerebro humano, visto en tres cuartos posterior; surcos y circunvoluciones complejos, membranas y vasos muy finos, color gris rosado natural. El córtex llena la mayor parte del encuadre; evitar un cerebro completo diminuto suspendido en un fondo vacío. Óptica virtual de 85–100 mm, profundidad de campo selectiva con zona focal suficiente para apreciar anatomía y un primer término suavemente desenfocado. Luz blanca suave arriba-izquierda, ribete azul izquierdo y violeta derecho; negros profundos, reflejos húmedos contenidos y ninguna superficie de plástico. Reconstrucción médica cinematográfica de alta gama, no neuroimagen funcional real. No representar el relleno como un agujero cerebral que se cierra, ni pedir al generador que reconstruya el punto. Remotion hará un avance 2.5D mínimo y la comparación perceptiva posterior explicará el mecanismo. Entrada tras la pregunta sobre el hueco negro; salida hacia PER conserva la paleta y el ritmo. Sin redes de neón, partículas ni texto.

### H — Visión binocular

Generar vídeo vertical 9:16, master de 8 segundos, con un tramo útil de 5,44 segundos. Primer plano de la región ocular de la misma persona ficticia de A, mostrando ambos ojos dentro del rostro, puente nasal y piel real; identidad, iris derecho, pestañas y posición de reflejos coherentes con la imagen maestra. El ojo derecho permanece abierto; el izquierdo, inicialmente cerrado, se abre una sola vez con movimiento natural durante la primera parte. Después ambos miran al mismo punto de fijación. Lente de retrato macro de 85 mm, profundidad de campo suficiente para ambos iris y fondo muy oscuro. Key blanca arriba-izquierda, acento azul izquierdo, recorte violeta derecho; materiales de piel y córnea fotorealistas de publicidad. Cámara realiza un dolly-in corto, sin órbita ni espejado. No generar campos visuales ni zonas faltantes: se añadirán en 2D con una correspondencia binocular controlada, sin HUD. Entrada desde el inserto de un ojo en A y salida a I mediante corte sobre el ojo derecho y conservación del eje. Sin parpadeos extra, asimetrías mutantes ni cambios de rostro.

### I — Plano final del ojo

Generar vídeo vertical 9:16, master de 8 segundos, con aproximadamente 5,07 segundos útiles. Volver al ojo derecho de la misma persona de A y H, con idéntico iris azul grisáceo, corona ámbar, párpados, venas y reflejo rectangular de pantalla. Primerísimo plano lleno, pupila situada por debajo del espacio de subtítulos y sin partes importantes cortadas de forma accidental. Lente macro de 100–120 mm, f/4–5.6 equivalente; iris nítido y periferia de piel desenfocada, córnea transparente y humedad sutil. Dolly-in suave, menor que en B; un ajuste de foco delicado acompaña el cierre y el movimiento se asienta antes del último sostén. Iluminación idéntica a A: blanco superior izquierdo, azul a izquierda y violeta a derecha, tejidos de color natural y negros profundos. Fotorealismo publicitario sin acabado plástico. Entrada por corte desde el ojo derecho de H, sin invertir orientación. La salida conserva el último encuadre bajo la cola original de voz; no hay parpadeo, fade ni acción añadida después de la frase. Sin textos ni elementos gráficos generados.

## Montaje posterior en Remotion

1. Referencias maestras: fijar identidad del ojo y del rostro; después fijar retina/disco/nervio con referencias anatómicas. Usar imágenes o fotogramas de referencia en los generadores que lo permitan; la continuidad no se confía únicamente al texto del prompt.
2. Aceptación visual antes de animar: comprobar iris, párpados, reflejos, capas retinales, disco y posición nasal. Rechazar fotogramas con anatomía incoherente o material plástico aunque sean vistosos.
3. Montaje por cues existentes: recortar los clips al timeline aprobado; conservar velocidad y muestras de la narración. No estirar voz, añadir frases ni volver a insertar la pausa.
4. Imágenes D1/D2/E1/F/G: recursos 2.5D de 1,5–2,5 s preferiblemente y nunca más de 3 s continuos por imagen. Alternar imágenes distintas, recortes, overlays explicativos y transiciones; evitar encadenar recortes como excusa para prolongar una foto. Los bloques largos se subdividen antes de producir. El experimento queda exceptuado y estático.
5. EXP: reutilizar exactamente SVG, colores, coordenadas y fotogramas de la lámina aprobada. Al aislar ese componente del módulo antiguo, verificar igualdad de píxeles; no arrastrar la escena de Three.js al nuevo montaje.
6. Explicación 2D: controlar proyección e inversión óptica, ausencia de respuesta en el disco, relleno del fondo sin recuperar el punto y contribución binocular con regiones faltantes diferentes. Sin dashboard ni marcos de interfaz decorativos. Las simulaciones perceptivas posteriores a 41,41 s se distinguen de la prueba real.
7. Subtítulos: reutilizar estilos, fragmentos y marcas temporales existentes, sin texto incrustado en los clips. Mantener una palabra resaltada por fragmento.
8. Transiciones: cortes por forma entre iris/pupila y retina, corte de escala para microscopía y corte sobre el eje para H/I. Fuera del experimento, evitar fundidos largos y cambios de dirección gratuitos; nunca deformar anatomía para conectar planos.
9. Sound design: voz en primer plano; whoosh corto y suave en la entrada, ambientes mínimos sólo cuando ayuden. Nada añadido durante la pausa ni efectos que interfieran con la prueba. El máster de voz queda intacto en una pista separada.
10. Revisión previa a exportar: contacto visual de todos los planos, continuidad de identidad y anatomía, prueba experimental idéntica, subtítulos y último gesto sincronizados con la locución. La referencia original sigue siendo el objetivo visual; el test de Blender no se usa como techo de calidad.
