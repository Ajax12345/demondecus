from bs4 import BeautifulSoup as soup
import typing, re

class LineObj:
    def __init__(self, _num:int, _octave:int, is_step:bool=False) -> None:
        self.num, self.octave, self.is_step = _num, _octave, is_step
    def __sub__(self, _new_note:dict) -> int:
        if self.num >= _new_note['position']:
            return (abs(self.num-_new_note['position'])+1)*2 - 1-int(self.is_step) +  int(_new_note['step'] == 'has_step'), self.num >= _new_note['position']
        return (abs(self.num-_new_note['position'])+1)*2 - 1-int(self.is_step) -  int(_new_note['step'] == 'has_step'), self.num >= _new_note['position']
    def __repr__(self) -> str:
        return f'Line({self.num}, {self.octave}, step={self.is_step})'

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
                return NoteFormat(a, _val['position'], b.octave, cls[_val['note']], _val['step'] == 'has_step')
            if not _d%8:
                return NoteFormat(a, _val['position'], b.octave+([-1, 1][_flag]*(_d//8)), cls[_val['note']], _val['step'] == 'has_step')

class Note(metaclass=NoteControl):
    headers = ['step', 'octave', 'note_type']
    note_placement = {'A':LineObj(6, 4), 'B':LineObj(6, 4, True), 'C':LineObj(5, 5), 'D':LineObj(8, 4), 'E':LineObj(8, 4, True), 'F':LineObj(7, 4), 'G':LineObj(7, 4, True)}
    type_converter = {'eighth_note':'eighth', 'quarter_note':'quarter', 'sixteenth_note':'16th', 'half_note':'half', 'whole_note':'whole'}
    def __init__(self, *args:typing.List[str]) -> None:
        self.__dict__ = dict(zip(self.__class__.headers, args))
    def __iter__(self) -> typing.Iterator:
        yield from [getattr(self, i) for i in self.__class__.headers]
    @property
    def line_num(self) -> dict:
        _note = self.__class__.note_placement[self.step]
        return {'line':abs(_note.num-(4*abs(int(_note.octave)-int(self.octave)))) + int(not _note.is_step if int(_note.octave) != int(self.octave) else 0), 'step':not _note.is_step if int(_note.octave) != int(self.octave) else _note.is_step}
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(step={self.step}, octave={self.octave}, type={self.note_type})'

class NoteGenerator:
    @classmethod
    def parse_file(cls, _name:str) -> typing.List[Note]:
        return [Note(*[getattr(getattr(i, c), 'text', None) for c in ['step', 'octave', 'type']]) for i in soup(open(f'datasets/{_name}.musicxml').read(), 'html.parser').find_all('note')]

if __name__ == '__main__':
    #_d = [i for i in NoteGenerator.parse_file('MozartTrio')]
    #print(_d[:10])
    #print([tuple(i) for i in _d[:10]])
    #print([i.line_num for i in _d[:10]])
    #print([tuple(i) for i in NoteGenerator.parse_file('MozartTrio')])
    #print([tuple(i) for i in NoteGenerator.parse_file('1_Marche_Slav_-_Tchaikovsky')])
    print(Note[{"note":"sixteenth_note","line":1,"position":5,"count":4,"step":"no_step"}])
