import os
from glob import glob

# Caminhos para as pastas de entrada e saída
INPUT_FOLDER = "input_samples"
OUTPUT_FOLDER = "output_result"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Lista de todas as notas a serem geradas
NOTES = ["a", "a_sharp", "b", "c", "c_sharp", "d", "d_sharp",
         "e", "f", "f_sharp", "g", "g_sharp"]

# Número total de oitavas
TOTAL_OCTAVES = 8

def pitch_factor(semitones):
    """Calcula o fator de ajuste para o tom."""
    return 2 ** (semitones / 12)

def generate_note(input_file, output_file, semitones):
    """Gera os arquivos de saída com ajuste de tom."""
    fator = pitch_factor(semitones)
    command = (
        f"ffmpeg -i {input_file} -af "
        f"asetrate=44100*{fator},aresample=44100 {output_file}"
    )
    os.system(command)

def map_input_files(input_folder):
    """Mapeia as notas de entrada."""
    input_files = glob(os.path.join(input_folder, "*.wav"))
    input_map = {}
    for input_file in input_files:
        base_name = os.path.basename(input_file)
        note, octave = parse_note_and_octave(base_name)
        input_map[(note, octave)] = input_file
    return input_map

def parse_note_and_octave(file_name):
    """Extrai a nota e a oitava do nome do arquivo."""
    note, octave = file_name.rsplit("_", 1)
    octave = int(octave.split(".")[0])
    return note, octave

def generate_output_notes():
    """Gera a lista de notas e oitavas a serem geradas."""
    output_notes = []
    for octave in range(1, TOTAL_OCTAVES + 1):
        for note in NOTES:
            output_notes.append((note, octave))
    return output_notes

def find_closest_input(input_map, target_note, target_octave, index):
    """Encontra o arquivo de entrada mais próximo."""
    closest_note = None
    closest_distance = float('inf')
    for (input_note, input_octave), input_file in input_map.items():
        distance = calculate_distance(input_note, input_octave, target_note, target_octave, index)
        if distance < closest_distance:
            closest_distance = distance
            closest_note = (input_note, input_octave, input_file)
    return closest_note

def calculate_distance(input_note, input_octave, target_note, target_octave, index):
    """Calcula a distância em semitons entre duas notas."""
    note_distance = (index // 12 - (input_octave - 1)) * 12
    note_distance += NOTES.index(target_note) - NOTES.index(input_note)
    return abs(note_distance)

def main():
    """Função principal para gerar as notas."""
    input_map = map_input_files(INPUT_FOLDER)
    output_notes = generate_output_notes()

    for index, (note, octave) in enumerate(output_notes):
        output_file = os.path.join(OUTPUT_FOLDER, f"{note}_{octave}.wav")
        if (note, octave) in input_map:
            # Copia o arquivo de entrada correspondente
            input_file = input_map[(note, octave)]
            os.system(f"cp {input_file} {output_file}")
        else:
            # Encontra o arquivo de entrada mais próximo
            closest_note = find_closest_input(input_map, note, octave, index)
            if closest_note:
                input_note, input_octave, input_file = closest_note
                semitones = (octave - input_octave) * 12
                semitones += NOTES.index(note) - NOTES.index(input_note)
                generate_note(input_file, output_file, semitones)

    print("Processo concluído! Todas as notas foram geradas e salvas na pasta output_result.")

if __name__ == "__main__":
    main()
