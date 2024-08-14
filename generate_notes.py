import os
import shutil
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
    command = (f'ffmpeg -hide_banner -loglevel error -i {origin_tone_path} '
               f'-af "rubberband=pitch=1.0595" '
               f'{generated_tone_path}')
    os.system(command)


def generate_a_semitone_lower(origin_tone_path, generated_tone_path):
    command = (f'ffmpeg -hide_banner -loglevel error -i {origin_tone_path} '
               f'-af "rubberband=pitch=0.9439" '
               f'{generated_tone_path}')
    os.system(command)


def generate_tones_asc(tones, origin):
    print(f'generate_tones_asc - Gerando os tons {tones} a partir de {origin}')

    origin_tone_path = f'{INPUT_FOLDER}/{origin}.wav'
    generated_tone_path = f'{OUTPUT_FOLDER}/{tones[0]}.wav'
    generate_a_semitone_higher(origin_tone_path, generated_tone_path)

    for i, _ in enumerate(tones):
        if (i + 1) == len(tones):
            break

        origin_tone = tones[i]
        generated_tone = tones[i + 1]
        generate_a_semitone_higher(
            f'{OUTPUT_FOLDER}/{origin_tone}.wav',
            f'{OUTPUT_FOLDER}/{generated_tone}.wav'
        )
        print('.', end='')

    print('\ngenerate_tones_asc - DONE\n')


def generate_tones_desc(tones, origin):
    print(f'generate_tones_desc - Gerando os tons {tones} a partir de {origin}')
    tones.reverse()

    # primeira geração usa a pasta input_samples, da segunda em diante usa a output_result
    # usando como origin o último áudio gerado no loop
    origin_tone_path = f'{INPUT_FOLDER}/{origin}.wav'
    generated_tone_path = f'{OUTPUT_FOLDER}/{tones[0]}.wav'
    generate_a_semitone_lower(origin_tone_path, generated_tone_path)

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

    print('\ngenerate_tones_desc - DONE\n')


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


def get_first_tones_until(first_input_note):
    all_tones = get_all_tones()
    first_input_note_idx = all_tones.index(first_input_note)
    return all_tones[0:first_input_note_idx]


def get_last_tones_from(last_input_note):
    all_tones = get_all_tones()
    last_input_note_idx = all_tones.index(last_input_note)
    return all_tones[(last_input_note_idx + 1):]


def copy_input_files_to_output_folder():
    print('Copiando input_samples para a pasta output_result')
    for filename in glob(os.path.join(INPUT_FOLDER, '*.wav')):
        shutil.copy(filename, OUTPUT_FOLDER)


def run():
    shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    input_notes = sort_musical_notes(get_input_notes())

    # Caso a primeira input note não for c_1 deverão ser gerados tons a partir de c_1 até a
    # primeira input_note mais grave
    if input_notes[0] != "c_1":
        origin = input_notes[0]
        first_tones = get_first_tones_until(origin)
        generate_tones_desc(first_tones, origin)

    # Continua gerando as notas, agora considerando os gaps existentes no array input_notes
    for i, input_note in enumerate(input_notes):
        if (i + 1) == len(input_notes):
            break
        tones_between = get_tones_between(input_note, input_notes[i + 1])
        generate_tones_asc(tones_between, input_note)

    # Semelhante ao início, caso a última input_note não for b_7 deverão ser gerados
    # tons a partir da última input_note até b_7
    if input_notes[-1] != "b_7":
        origin = input_notes[-1]
        last_tones = get_last_tones_from(origin)
        generate_tones_asc(last_tones, origin)

    copy_input_files_to_output_folder()

    print('Done!')


if __name__ == "__main__":
    run()
