import os


def replace_word_in_file(file_path, old_word, new_word):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace(old_word, new_word)

    with open(file_path, 'w') as file:
        file.write(content)


def process_txt_files(directory, old_word, new_word):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            replace_word_in_file(file_path, old_word, new_word)
            print(f"Word replaced in {file_path}")


# Replace these values with your actual directory and words
directory_path = 'datasets/OIDv4/OID/Dataset/train/labels'
old_words_to_replace = ['Cat', 'Dog', 'Jaguar']
new_word = ['1', '2', '3']

for idx, old_word in enumerate(old_words_to_replace):
    process_txt_files(directory_path, old_word, new_word[idx])
