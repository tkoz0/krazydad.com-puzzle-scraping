'''
Parser for the 1 per page sudoku pdfs. Outputs 1 JSON object per line to stdout.
Set INPUT_DIR to be the directory with the xml files from pdf2txt.py
Then run "python3 parseSudoku1pp.py > output.jsonl"
'''

import os
from typing import Dict, List, Tuple
import bs4
import tqdm
import re
import json
import sys
import bz2

INPUT_DIR = 'sudoku1pp_xml_tmp'

# groups: difficulty, volume, book
FNAME_RE = re.compile(r'KD_Sudoku_([A-Z][A-Z])(\d*)_8_v(\d+).xml.bz2')

# all 81 possible cell text positions
# (x0,y0,x1,y1), bottom left is (0,0), box is (x0,y0),(x1,y1) where x0<x1,y0<y1
POSITIONS = {
'332.493,364.126,350.285,401.118', '332.493,408.015,350.285,445.007', '332.493,627.459,350.285,664.451',
'200.826,539.682,218.618,576.674', '288.604,364.126,306.396,401.118', '332.493,320.237,350.285,357.229',
'200.826,364.126,218.618,401.118', '156.937,451.904,174.729,488.896', '156.937,364.126,174.729,401.118',
'464.160,583.570,481.952,620.562', '288.604,539.682,306.396,576.674', '244.715,495.793,262.507,532.785',
'113.048,276.348,130.840,313.340', '113.048,495.793,130.840,532.785', '156.937,539.682,174.729,576.674',
'200.826,583.570,218.618,620.562', '244.715,583.570,262.507,620.562', '113.048,408.015,130.840,445.007',
'464.160,364.126,481.952,401.118', '376.382,627.459,394.174,664.451', '420.271,451.904,438.063,488.896',
'376.382,495.793,394.174,532.785', '156.937,408.015,174.729,445.007', '376.382,276.348,394.174,313.340',
'200.826,408.015,218.618,445.007', '113.048,320.237,130.840,357.229', '288.604,495.793,306.396,532.785',
'113.048,451.904,130.840,488.896', '420.271,495.793,438.063,532.785', '332.493,451.904,350.285,488.896',
'464.160,408.015,481.952,445.007', '376.382,539.682,394.174,576.674', '244.715,408.015,262.507,445.007',
'376.382,364.126,394.174,401.118', '244.715,451.904,262.507,488.896', '156.937,276.348,174.729,313.340',
'420.271,539.682,438.063,576.674', '288.604,583.570,306.396,620.562', '200.826,627.459,218.618,664.451',
'464.160,539.682,481.952,576.674', '332.493,495.793,350.285,532.785', '420.271,627.459,438.063,664.451',
'156.937,583.570,174.729,620.562', '288.604,451.904,306.396,488.896', '244.715,539.682,262.507,576.674',
'332.493,276.348,350.285,313.340', '420.271,320.237,438.063,357.229', '464.160,320.237,481.952,357.229',
'464.160,276.348,481.952,313.340', '288.604,320.237,306.396,357.229', '464.160,495.793,481.952,532.785',
'200.826,320.237,218.618,357.229', '244.715,320.237,262.507,357.229', '244.715,276.348,262.507,313.340',
'113.048,539.682,130.840,576.674', '332.493,539.682,350.285,576.674', '288.604,408.015,306.396,445.007',
'420.271,276.348,438.063,313.340', '156.937,627.459,174.729,664.451', '200.826,495.793,218.618,532.785',
'288.604,276.348,306.396,313.340', '156.937,495.793,174.729,532.785', '200.826,276.348,218.618,313.340',
'113.048,583.570,130.840,620.562', '200.826,451.904,218.618,488.896', '376.382,583.570,394.174,620.562',
'376.382,451.904,394.174,488.896', '244.715,627.459,262.507,664.451', '420.271,408.015,438.063,445.007',
'376.382,408.015,394.174,445.007', '113.048,627.459,130.840,664.451', '420.271,583.570,438.063,620.562',
'288.604,627.459,306.396,664.451', '464.160,627.459,481.952,664.451', '156.937,320.237,174.729,357.229',
'376.382,320.237,394.174,357.229', '113.048,364.126,130.840,401.118', '420.271,364.126,438.063,401.118',
'244.715,364.126,262.507,401.118', '332.493,583.570,350.285,620.562', '464.160,451.904,481.952,488.896'}

# sort by y0 decreasing, then x0 increasing
def _pos_sort(p):
    x0,y0,_,_ = map(float,p.split(','))
    return 100000000*(-y0)+x0

# build mapping of position to cell row,col coordinate
POS_MAP: Dict[str,Tuple[int,int]] = dict()
_pos_tmp = sorted(POSITIONS, key=_pos_sort)

for r in range(9):
    for c in range(9):
        POS_MAP[_pos_tmp[9*r+c]] = (r,c)

def extract_text(xml: bs4.BeautifulSoup) -> List[Dict[str,str]]:
    # expects 8 pages with puzzles (id=1,2,3,4,5,6,7,8)
    # (9 and 10 are hints and answers, do not care about those)
    # page num -> page object
    pages = {page.attrs['id']: page for page in xml.findAll('page')}
    assert len(pages) == 10
    result: List[Dict[str,str]] = [] # for each puzzle (1..8) the (position -> digit) mapping
    for page in range(1,9):
        page = pages[str(page)]
        # sudoku cells have font="Helvetica" and size="36.992"
        raw_cells = page.findAll('text',attrs={'font':'Helvetica','size':'36.992'})
        # position -> digit
        cells: Dict[str,str] = {cell.attrs['bbox']: cell.text for cell in raw_cells}
        # sanity check
        assert 16 <= len(cells) <= 50
        for v in cells.values():
            assert len(v) == 1 and v in '123456789'
        result.append(cells)
    return result

# brute force sudoku solver
def solve_recur(puzzle: List[List[int]], pos: int) -> List[List[List[int]]]:
    if pos == 81:
        return [[row[:] for row in puzzle]]
    r,c = divmod(pos,9)
    br,bc = (r//3)*3, (c//3)*3 # upper left of block
    if puzzle[r][c] != 0:
        return solve_recur(puzzle,pos+1)
    digits = [True]*10 # digits possible in cell
    for i in range(9):
        digits[puzzle[r][i]] = False # row
        digits[puzzle[i][c]] = False # col
        digits[puzzle[br+(i//3)][bc+(i%3)]] = False # block
    solns = []
    for d in range(1,10): # try digits
        if not digits[d]:
            continue
        puzzle[r][c] = d
        solns += solve_recur(puzzle,pos+1)
        if len(solns) > 1: # error if multiple solutions
            break
    puzzle[r][c] = 0 # backtrack
    return [] if len(solns) > 1 else solns

files = os.listdir(INPUT_DIR)

for file in tqdm.tqdm(files):
    match = FNAME_RE.fullmatch(file)
    assert match
    dif,vol,book = match.groups()
    tqdm.tqdm.write('parsing: '+file+' (dif = %s, vol = %d, book = %d)'%(dif, 1 if vol == '' else int(vol), int(book)), sys.stderr)
    file = INPUT_DIR+'/'+file
    xml = bs4.BeautifulSoup(bz2.open(file,'r').read(),features='xml')
    text = extract_text(xml)
    for p,page in enumerate(text):
        #tqdm.tqdm.write('- puzzle '+str(p+1), sys.stderr)
        puzzle = [[0]*9 for _ in range(9)]
        for pos,digit in page.items():
            digit = int(digit)
            r,c = POS_MAP[pos]
            assert puzzle[r][c] == 0
            assert 1 <= digit <= 9
            puzzle[r][c] = int(digit)
        solns = solve_recur(puzzle,0)
        assert len(solns) == 1
        # convert to string of 81 chars
        puzzle_str = ''.join(''.join(map(str,row)) for row in puzzle)
        puzzle_json = json.dumps({
            'dif': dif,
            'vol': 1 if vol == '' else int(vol),
            'book': int(book),
            'num': p+1,
            'puzzle': puzzle_str
        }, separators=(',',':'))
        print(puzzle_json)
