import os.path
import sys


class DirectFolder:
    _files_cache = dict()

    def __str__(self):
        return self.files().__str__()

    def __init__(self, name):
        self.dir_path = os.path.abspath(name)
        self.update()

    def makes(self, t: dict[str, any]):
        if os.path.isdir(self.dir_path):
            for k, v in t.items():
                file = open(os.path.join(self.dir_path, k), 'w+')
                if not file:
                    raise OSError('Cannot access a folder / file!')
                self._files_cache[k] = v
                if file.read() is not v:
                    file.write(str(v))
                    file.close()
        else:
            raise FileNotFoundError(f'Directory {self.dir_path} does not exist!')

    def files(self) -> dict[str, any, int]:
        return self._files_cache

    def reads(self, t: list[str]) -> list[str]:
        out = dict()
        for i in t:
            out[i] = self._files_cache[i]

        return out

    def renames(self, t: list[str]):
        for i in t:
            name = i.split('>')
            os.renames(os.path.join(self.dir_path, name[0]), os.path.join(self.dir_path, name[1]))
        self.update()

    def unlinks(self, t: list[str]):
        arr = t.copy()
        for i, v in enumerate(arr):
            _pth = os.path.join(self.dir_path, v)
            if os.path.isfile(_pth):
                os.unlink(_pth)
                del self._files_cache[v]
            else:
                raise OSError(f'File {_pth} is unreachable or not exist')
        del arr

    def update(self):
        self._files_cache = dict()
        for i in os.scandir(self.dir_path):
            file = open(os.path.join(self.dir_path, i.name), 'r')
            self._files_cache[i.name] = file.read()
            file.close()

    def clear(self):
        self.unlinks(self._files_cache)

    def destroy(self):
        if os.path.isdir(self.dir_path):
            self.unlinks([i for i in self.files()])

            os.rmdir(self.dir_path)
        else:
            raise OSError('Not a folder')
