import os
import subprocess
from glob import glob

TOTAL_OCTAVES = 7
TONES = ["c", "c_sharp", "d", "d_sharp", "e", "f", "f_sharp", "g", "g_sharp", "a", "a_sharp", "b"]
INPUT_FOLDER = "input_samples"
OUTPUT_FOLDER = "output_result"


def get_all_tones():
    result = []
    for octave in range(1, TOTAL_OCTAVES + 1):
        for tone in TONES:
            result.append(f"{tone}_{octave}")

    return result


def get_input_notes():
    input_files = glob(os.path.join(INPUT_FOLDER, "*.wav"))
    return [os.path.basename(file).replace('.wav', '') for file in input_files]


def get_tones_between(start_note=None, end_note=None, ascending=True):
    all_tones = get_all_tones()
    try:
        if start_note is not None:
            start_index = all_tones.index(start_note) + 1
        else:
            start_index = 0

        if end_note is not None:
            end_index = all_tones.index(end_note)
        else:
            end_index = len(all_tones)

        if start_index < end_index:
            notes_range = all_tones[start_index:end_index]
        else:
            notes_range = all_tones[end_index:start_index][::-1]

        return notes_range if ascending else notes_range[::-1]

    except ValueError:
        return "Uma ou ambas as notas fornecidas não existem no array all_tones."


def generate_a_semitone_higher(origin_tone_path, generated_tone_path):
    command = (f'ffmpeg -hide_banner -i {origin_tone_path} '
               f'-af "rubberband=pitch=1.0595" '
               f'{generated_tone_path}')
    os.system(command)


def generate_a_semitone_lower(origin_tone_path, generated_tone_path):
    command = (f'ffmpeg -hide_banner -loglevel error -i {origin_tone_path} '
               f'-af "rubberband=pitch=0.9439" '
               f'{generated_tone_path}')
    os.system(command)


def generate_tones_asc(tones):
    for _, i in enumerate(tones):
        origin_tone = tones[i]
        generated_tone = tones[i + 1]
        generate_a_semitone_higher(origin_tone, generated_tone)


def generate_tones_desc(tones, origin):
    print(f'generate_tones_desc - Gerando os tons {tones} a partir de {origin}')

    tones.reverse()

    # A primeira geração considera o origin como o arquivo que veio da pasta input_samples
    generated_tone = tones[0]
    generate_a_semitone_lower(
        f'{INPUT_FOLDER}/{origin}.wav',
        f'{OUTPUT_FOLDER}/{generated_tone}.wav'
    )

    # Da segunda geração em diante considera o origin como os da pasta
    # output_result que vão ir sendo gerados no loop
    for i, _ in enumerate(tones):
        if (i + 1) == len(tones):
            break

        origin_tone = tones[i]
        generated_tone = tones[i + 1]
        generate_a_semitone_lower(
            f'{OUTPUT_FOLDER}/{origin_tone}.wav',
            f'{OUTPUT_FOLDER}/{generated_tone}.wav'
        )
        print('.', end='')

    print('\ngenerate_tones_desc - DONE')


def sort_musical_notes(notes):
    note_order = [
        'c', 'c_sharp', 'd', 'd_sharp', 'e', 'f', 'f_sharp',
        'g', 'g_sharp', 'a', 'a_sharp', 'b'
    ]

    def note_key(note):
        parts = note.rsplit('_', 1)
        note_part = parts[0]
        octave = int(parts[1])
        note_index = note_order.index(note_part)
        return octave, note_index

    sorted_notes = sorted(notes, key=note_key)
    return sorted_notes


def get_first_tones_between(input_notes):
    all_tones = get_all_tones()
    first_input_note_idx = all_tones.index(input_notes[0])
    return all_tones[0:first_input_note_idx]


def main():
    input_notes = sort_musical_notes(get_input_notes())

    # Caso a primeira input note não for c_1 já devem ser gerados tons a partir de c_1 até a
    # primeira nota mais grave (que é mais aguda que c_1)
    if input_notes[0] != "c_1":
        origin = input_notes[0]
        first_tones = get_first_tones_between(input_notes)
        generate_tones_desc(first_tones, origin)

    # Continua gerando as notas, agora considerando os gaps existentes no array input_notes
    # for i, input_note in enumerate(input_notes):
    #     tones_between = get_tones_between(input_note, input_notes[i + 1])
    #     generate_tones_asc(tones_between)

    # TODO: Assim como o início será preciso gerar os tons que restarem entre a última
    #  input_note e a última nota definitiva (b_7)


if __name__ == "__main__":
    main()
