import os
import shutil
import json
import zipfile

# Variáveis de configuração
APP_KITS_FOLDER = "/home/antonio/Documents/oliveira-labs/megapiano-kits"
GENERATED_SAMPLES_FOLDER = "/home/antonio/Documents/oliveira-labs/utils/samples-generator/output_result"


def create_next_kit_folder(kit_name):
    # 1. Obtenha o próximo número de pasta
    next_folder_number = get_next_folder_number()
    print(f"Próxima pasta será: {next_folder_number}")

    # 2. Crie a pasta no diretório APP_KITS_FOLDER
    new_kit_folder = os.path.join(APP_KITS_FOLDER, str(next_folder_number))
    os.makedirs(new_kit_folder, exist_ok=True)
    print(f"Pasta criada: {new_kit_folder}")

    # 3. Crie a subpasta 'megapianokit' e o arquivo kit.json
    megapianokit_folder = os.path.join(new_kit_folder, "megapianokit")
    os.makedirs(megapianokit_folder, exist_ok=True)
    print(f"Subpasta 'megapianokit' criada em: {megapianokit_folder}")

    kit_json_path = os.path.join(megapianokit_folder, "kit.json")
    with open(kit_json_path, 'w') as kit_file:
        json.dump({"name": kit_name}, kit_file)
    print(f"Arquivo kit.json criado com o conteúdo: {{'name': '{kit_name}'}}")

    # 4. Mova os arquivos do OUTPUT_FOLDER para a pasta 'megapianokit'
    move_files_to_folder(GENERATED_SAMPLES_FOLDER, megapianokit_folder)

    # 5. Compacte a pasta 'megapianokit' e renomeie para 'kit.megapiano'
    create_kit_archive(megapianokit_folder)

    # 6. Apague a pasta 'megapianokit' e todo seu conteúdo
    shutil.rmtree(megapianokit_folder)
    print(f"Subpasta 'megapianokit' removida, mantendo apenas o arquivo 'kit.megapiano'")


def get_next_folder_number():
    # Obtenha o número da próxima pasta com base no maior número existente
    folders = [int(name) for name in os.listdir(APP_KITS_FOLDER) if name.isdigit()]
    return max(folders, default=0) + 1


def move_files_to_folder(source_folder, target_folder):
    # Mova todos os arquivos da pasta source_folder para target_folder
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        target_file = os.path.join(target_folder, filename)
        shutil.move(source_file, target_file)
    print(f"Arquivos movidos de {source_folder} para {target_folder}")


def create_kit_archive(folder_path):
    # Crie um arquivo zip da pasta e renomeie para .megapiano
    archive_path = shutil.make_archive(folder_path, 'zip', folder_path)
    renamed_archive = archive_path.replace('.zip', '.megapiano')
    os.rename(archive_path, renamed_archive)
    print(f"Arquivo compactado criado: {renamed_archive}")


# Execução do script
if __name__ == "__main__":
    kit_name = "NomeDoKit"  # Defina o nome do kit aqui ou receba como input
    create_next_kit_folder(kit_name)
