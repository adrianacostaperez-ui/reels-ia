#!/usr/bin/env python3
"""Prepare an audition candidate; never substitutes a local robotic voice."""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAD = .20


def aligned_timeline(response, template):
    alignment = response.get('alignment') or response.get('normalized_alignment')
    if not alignment:
        raise ValueError('El servicio no ha devuelto alineación; no se inventarán tiempos.')
    chars = alignment['characters']
    starts = alignment['character_start_times_seconds']
    ends = alignment['character_end_times_seconds']
    text = ''.join(chars)
    if text != template['text'] or not len(chars) == len(starts) == len(ends):
        raise ValueError('La alineación no coincide con el guion exacto. Revisar la toma.')
    if any(a < 0 or b < a for a, b in zip(starts, ends)):
        raise ValueError('Timestamps inválidos.')
    words = [{'text':m.group(), 'start':LEAD + starts[m.start()],
              'end':LEAD + ends[m.end()-1]} for m in re.finditer(r'\S+', text)]
    if len(words) != 19:
        raise ValueError('Número de palabras inesperado.')
    result = dict(template)
    groups = [(0,4,'móvil'),(4,5,'exactamente'),(5,8,'batería'),
              (8,10,'realidad'),(10,13,'chip'),(13,19,'calcula')]
    captions=[]
    for a,b,highlight in groups:
        start,end=words[a]['start'],words[b-1]['end']+.07
        captions.append({'text':' '.join(w['text'] for w in words[a:b]).rstrip('. ,'),
                         'highlight':highlight,'start':start,'end':end,
                         'from':round(start*30),'to':round(end*30)})
    result.update(words=words,captions=captions,voice='ElevenLabs — toma candidata pendiente de escucha',
                  voiceStatus='candidate_needs_listening',timingStatus='aligned_to_candidate',
                  chipStart=round(words[10]['start']*30),chipWord=round(words[12]['start']*30),
                  chipEnd=round(words[12]['end']*30),pulseStart=round(words[13]['start']*30),
                  voiceEnd=words[-1]['end'],audioLeadSeconds=LEAD)
    if result['voiceEnd'] > 7.65:
        result.update(voiceStatus='candidate_needs_pacing_review',fitsEightSeconds=False)
    else:
        result['fitsEightSeconds']=True
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--check',action='store_true',help='Validación local; no utiliza la red.')
    modes.add_argument('--generate',action='store_true',help='Solicita una toma al servicio configurado.')
    args=parser.parse_args()
    body=json.loads((HERE/'peticion-tts.json').read_text())
    template=json.loads((HERE/'timing.json').read_text())
    exact=' '.join((HERE/'guion.txt').read_text().split())
    if body['text'] != template['text'] or body['text'] != exact:
        raise ValueError('Guion, petición y timing deben coincidir exactamente.')
    if body['voice_settings']['speed'] != 1.0:
        raise ValueError('La preparación debe conservar la velocidad natural de la voz.')
    if args.check:
        print('Preparación correcta: guion exacto, 19 palabras, sin voz local ni cambio de tempo. No se ha enviado ninguna petición.')
        return
    key=os.environ.get('ELEVENLABS_API_KEY')
    voice=os.environ.get('ELEVENLABS_VOICE_ID')
    if not key or not voice:
        raise ValueError('Falta configurar ELEVENLABS_API_KEY y/o ELEVENLABS_VOICE_ID en el entorno. No poner sus valores en el chat.')
    endpoint='https://api.elevenlabs.io/v1/text-to-speech/'+urllib.parse.quote(voice,safe='')+'/with-timestamps?output_format=mp3_44100_128'
    request=urllib.request.Request(endpoint,data=json.dumps(body).encode(),headers={'xi-api-key':key,'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(request,timeout=90) as stream:
            response=json.load(stream)
    except urllib.error.HTTPError as error:
        raise ValueError(f'ElevenLabs devolvió HTTP {error.code}. Revisar acceso, red o plan; no se ha sustituido la voz.') from None
    audio=base64.b64decode(response['audio_base64'],validate=True)
    if len(audio)<1024:
        raise ValueError('La pista recibida está vacía o incompleta.')
    # Preserve the audition even if its natural duration does not fit the target.
    path=HERE/'toma-candidata.mp3'
    if path.exists():
        raise ValueError('Ya existe toma-candidata.mp3. Conservarla o renombrarla antes de generar otra.')
    timeline=aligned_timeline(response,template)
    path.write_bytes(audio)
    (HERE/'timing-alineado.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
    print('Toma candidata y tiempos reales guardados por separado. Escuchar antes de aprobar; el borrador y los MP4 no se han sustituido.')
    if not timeline['fitsEightSeconds']:
        print('La toma no cabe naturalmente en ocho segundos. No se ha acelerado ni recortado.')


if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,urllib.error.URLError) as error:
        print(str(error),file=sys.stderr)
        sys.exit(1)
