import os
import shutil


def move_files(file_path, destination_folder, threshold_length=4):
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder, exist_ok=True)

    # Check if it's a file and not a directory
    if os.path.isfile(file_path):
        filename = os.path.basename(file_path)
        destination_path = os.path.join(destination_folder, filename)
        shutil.move(file_path, destination_path)
        print(f'Moved: {file_path}')


def move_data_without_label(file_path):
    destination_folder = file_path.replace(
        "\\", "/").split("/")
    destination_folder.pop()  # Remove file name
    last_folder = destination_folder.pop()
    destination_folder.append("empty_label")
    destination_folder.append(last_folder)
    destination_folder = ("/").join(destination_folder)

    move_files(file_path, destination_folder)
    move_files(file_path.replace("labels", "images").replace(
        "txt", "jpg"), destination_folder.replace("labels", "images"))


def replace_first_number_in_file(file_path, new_word):
    with open(file_path, 'r') as file:
        content = file.read()
    lines = content.split("\n")

    splitted = []
    for line in lines:
        new_line = new_word + line[1:]
        splitted.append(new_line)

    new_content = ("\n").join(splitted)

    if len(new_content) < 4:
        move_data_without_label(file_path)
        return

    with open(file_path, 'w') as file:
        file.write(new_content)


def replace_word_in_file(file_path, old_word, new_word):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace(old_word, new_word)

    with open(file_path, 'w') as file:
        file.write(content)


def process_txt_files(directory, old_word, new_word, replace_first_number=False):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            if replace_first_number:
                replace_first_number_in_file(file_path, new_word)
            else:
                replace_word_in_file(file_path, old_word, new_word)
            print(f"Word replaced in {file_path}")


# Replace these values with your actual directory and words
# directory_path = 'datasets/OIDv4/OID/Dataset/train/labels'
# old_words_to_replace = ['Cat', 'Dog', 'Jaguar']
# new_word = ['2', '1', '3']
# directory_path = 'datasets/OIDv4/OID/lu/train/labels'
# directory_path = 'datasets/OIDv4/OID/lu/Batch 2 - Dogs and Cats/Cats/validation/labels'
data_types = ["train", "test", "validation"]
path = 'datasets\OIDv4\OID\lu\Batch 3 - Dogs and Cats\Dogs/{type}/labels'
old_words_to_replace = ['Dog']
new_word = ["1"]
replace_first_number = True

for data_type in data_types:
    directory_path = path.replace("{type}", data_type)

    for idx, old_word in enumerate(old_words_to_replace):
        process_txt_files(directory_path, old_word,
                          new_word[idx], replace_first_number)
