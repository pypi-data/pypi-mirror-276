from os import walk
from terminal import print_in_color

def files_list(path, subfolders=False, paths_only=False):
    class File:
        def __init__(self, file, folder) -> None:
            self.full_name = file
            self.name = self.full_name.split('.', 1)[0]
            self.ext = '.' + self.full_name.rsplit('.', 1)[-1]
            self.path = f'{folder}\\{file}'
            self.folder_path = folder
            self.folder_name = folder.rsplit('\\', 1)[-1]

    предварительный_список = list(walk(path))
    if len(предварительный_список) == 0:
        print_in_color('Такой папки не существует', red=True)
        return []

    if subfolders:
        все_папки = предварительный_список
    else:
        все_папки = [предварительный_список[0]]

    res = []
    for список in все_папки:
        корневая_папка = список[0]
        файлы = список[2]
        if paths_only:
            for файл in файлы:
                res.append(f'{корневая_папка}\\{файл}')
            continue

        for файл in файлы:
            res.append(File(файл, корневая_папка))

    return res

if __name__ == '__main__':
    res = files_list(r'C:\Dev\tools', subfolders=True)
    for file in res:
        print(file.path)