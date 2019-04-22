from bs4 import BeautifulSoup as soup
import typing, re, contextlib, json
import os, itertools
from sklearn.naive_bayes import GaussianNB

class LineObj:
    def __init__(self, _num:int, _octave:int, is_step:bool=False) -> None:
        self.num, self.octave, self.is_step = _num, _octave, is_step
    def __sub__(self, _new_note:dict) -> int:
        if self.num >= _new_note['position']:
            return (abs(self.num-_new_note['position'])+1)*2 - 1-int(self.is_step) +  int(_new_note['step'] == 'has_step'), self.num >= _new_note['position']
        return (abs(self.num-_new_note['position'])+1)*2 - 1-int(self.is_step) -  int(_new_note['step'] == 'has_step'), self.num >= _new_note['position']
    def __repr__(self) -> str:
        return f'Line({self.num}, {self.octave}, step={self.is_step})'


class _note:
    headers = ['step', 'octave', 'note_type']
    note_placement = {'A':LineObj(6, 4), 'B':LineObj(6, 4, True), 'C':LineObj(5, 5), 'D':LineObj(8, 4), 'E':LineObj(8, 4, True), 'F':LineObj(7, 4), 'G':LineObj(7, 4, True)}
    type_converter = {'eighth_note':'eighth', 'quarter_note':'quarter', 'sixteenth_note':'16th', 'half_note':'half', 'whole_note':'whole'}
    def __init__(self, *args:typing.List[str]) -> None:
        self.__dict__ = dict(zip(self.__class__.headers, args))
    @property
    def line_num(self) -> dict:
        _note = self.__class__.note_placement[self.step]
        return {'line':abs(_note.num-(4*abs(int(_note.octave)-int(self.octave)))) + int(not _note.is_step if int(_note.octave) != int(self.octave) else 0), 'step':not _note.is_step if int(_note.octave) != int(self.octave) else _note.is_step} 
    def __eq__(self, n) -> bool:
        return all(str(getattr(self, i)) == str(getattr(n, i)) for i in self.__class__.headers)
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__})'

@contextlib.contextmanager
def get_notes() -> typing.Dict[int, _note]:
    with open('note_hashes.json') as f:
        yield {int(a):_note(*b) for a, b in json.load(f).items()}
    
with get_notes() as all_notes:
    all_notes = {a+1:b for a, b in all_notes.items()}

class NoteFormat:
    def __init__(self, _name:str, _num:int, _octave:int, _note_name:str, _is_step:bool) -> None:
        self.name, self.num, self.octave, self.note_name, self.is_step = _name, _num, _octave, _note_name, _is_step
    def __iter__(self):
        yield (self.name, str(self.octave), self.note_name)
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__})'

class NoteControl(type):
    def __getitem__(cls, _val:typing.Tuple[dict, str]) -> typing.Tuple[tuple, str]:
        if isinstance(_val, str):
            return cls.type_converter[re.sub('^dotted_', '', _val)]
        for a, b in cls.note_placement.items():
            _d, _flag = b - _val
            if _d == 1:
                return cls(a, b.octave, cls[_val['note']])
            if not _d%8:
                #return (a, LineObj(_val['position'], b.octave+(_d//8), _val['step'] == 'has_step'))
                return cls(a, b.octave+([-1, 1][_flag]*(_d//8)), cls[_val['note']])

class Note(_note, metaclass=NoteControl):
    def __iter__(self) -> typing.Iterator:
        yield from [getattr(self, i) for i in self.__class__.headers]
    def __len__(self) -> int:
        _c = [a for a, b in all_notes.items() if b == self]
        return 0 if not _c else _c[0]
    def __contains__(self, _note_name:str) -> bool:
        return self.note_type == _note_name
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(step={self.step}, octave={self.octave}, type={self.note_type})'
    

class NoteGenerator:
    @classmethod
    def parse_file(cls, _name:str, must_have=_note.type_converter.values()) -> typing.List[Note]:
        _c = [Note(*[getattr(getattr(i, c), 'text', None) for c in ['step', 'octave', 'type']]) for i in soup(open(f'datasets/{_name}.musicxml').read(), 'html.parser').find_all('note')]
        return [i for i in _c if any(h in i for h in must_have)]
    @classmethod
    def get_note(cls, _notes:typing.List[dict], _dataset:int) -> dict:
        t = list(filter(None, [Note[i] for i in sorted(_notes, key=lambda x:x['count'])]))
        _n = list(filter(None, [len(i) for i in t if i is not None]))
        _files = [i for i in os.listdir('datasets') if i.endswith('.json') and i.startswith(str(_dataset))]
        all_data = [i for b in _files for i in json.load(open(f'datasets/{b}'))]
        l = len(_n[:10])
        grouped = [all_data[i:i+l+1] for i in range(0, len(all_data), l+1)]
        _m = len(max(grouped, key=len))
        *data, results = [i for i in zip(*[i for i in grouped if len(i) == _m])]
        data = list(zip(*data))
        model = GaussianNB()
        model.fit(data, results)
        final_note = all_notes[int(model.predict([_n[-l:]])[0])]
        return {'note':{**final_note.line_num, 'type':final_note.note_type}}
    
if __name__ == '__main__':
    #_d = [len(i) for i in NoteGenerator.parse_file('MozartTrio') if all(i)]
    #print(_d)
    #print(_d)
    #print(_d[:10])
    #print([tuple(i) for i in _d[:10]])
    #print([i.line_num for i in _d[:10]])
    #print([tuple(i) for i in NoteGenerator.parse_file('MozartTrio')])
    #print([tuple(i) for i in NoteGenerator.parse_file('1_Marche_Slav_-_Tchaikovsky')])
    print(Note[{"note":"sixteenth_note","line":1,"position":5,"count":4,"step":"has_step"}])
    
