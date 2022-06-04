'''
Parser for the 1 per page sudoku pdfs. Outputs a CSV file to stdout.
Set INPUT_DIR to be the directory with the xml files from pdf2txt.py
Then run "python3 parseSudoku1pp.py > output.csv"
'''

import os
from typing import Dict, List, Tuple, Union
import bs4
import tqdm
import re
import json
import sys
import bz2

INPUT_DIR = 'sudoku1pp_xml'

# groups: difficulty, volume, book
FNAME_RE = re.compile(r'KD_Sudoku_([A-Z][A-Z])(\d*)_8_v(\d+).xml.bz2')

# all 81 possible cell text positions for both cases (with/without scratch space)
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
POSITIONS2 = {
'464.160,414.126,481.952,451.118', '156.937,545.793,174.729,582.785', '332.493,326.348,350.285,363.340',
'420.271,414.126,438.063,451.118', '244.715,501.904,262.507,538.896', '156.937,458.015,174.729,495.007',
'200.826,414.126,218.618,451.118', '420.271,545.793,438.063,582.785', '420.271,458.015,438.063,495.007',
'156.937,326.348,174.729,363.340', '113.048,326.348,130.840,363.340', '376.382,414.126,394.174,451.118',
'244.715,677.459,262.507,714.451', '156.937,370.237,174.729,407.229', '420.271,501.904,438.063,538.896',
'420.271,589.682,438.063,626.674', '288.604,633.570,306.396,670.562', '288.604,370.237,306.396,407.229',
'332.493,545.793,350.285,582.785', '200.826,545.793,218.618,582.785', '376.382,370.237,394.174,407.229',
'332.493,370.237,350.285,407.229', '244.715,458.015,262.507,495.007', '376.382,501.904,394.174,538.896',
'464.160,677.459,481.952,714.451', '332.493,589.682,350.285,626.674', '288.604,589.682,306.396,626.674',
'156.937,589.682,174.729,626.674', '156.937,414.126,174.729,451.118', '200.826,326.348,218.618,363.340',
'200.826,677.459,218.618,714.451', '420.271,326.348,438.063,363.340', '200.826,501.904,218.618,538.896',
'156.937,677.459,174.729,714.451', '464.160,458.015,481.952,495.007', '200.826,589.682,218.618,626.674',
'376.382,545.793,394.174,582.785', '156.937,501.904,174.729,538.896', '376.382,589.682,394.174,626.674',
'200.826,458.015,218.618,495.007', '113.048,545.793,130.840,582.785', '288.604,677.459,306.396,714.451',
'156.937,633.570,174.729,670.562', '113.048,633.570,130.840,670.562', '420.271,633.570,438.063,670.562',
'288.604,414.126,306.396,451.118', '113.048,370.237,130.840,407.229', '420.271,370.237,438.063,407.229',
'376.382,458.015,394.174,495.007', '464.160,589.682,481.952,626.674', '244.715,633.570,262.507,670.562',
'288.604,501.904,306.396,538.896', '244.715,545.793,262.507,582.785', '332.493,414.126,350.285,451.118',
'244.715,414.126,262.507,451.118', '376.382,677.459,394.174,714.451', '464.160,370.237,481.952,407.229',
'113.048,677.459,130.840,714.451', '200.826,370.237,218.618,407.229', '288.604,458.015,306.396,495.007',
'113.048,501.904,130.840,538.896', '244.715,370.237,262.507,407.229', '376.382,633.570,394.174,670.562',
'464.160,545.793,481.952,582.785', '288.604,545.793,306.396,582.785', '332.493,633.570,350.285,670.562',
'113.048,414.126,130.840,451.118', '464.160,326.348,481.952,363.340', '332.493,458.015,350.285,495.007',
'113.048,458.015,130.840,495.007', '244.715,589.682,262.507,626.674', '376.382,326.348,394.174,363.340',
'288.604,326.348,306.396,363.340', '200.826,633.570,218.618,670.562', '420.271,677.459,438.063,714.451',
'332.493,501.904,350.285,538.896', '244.715,326.348,262.507,363.340', '332.493,677.459,350.285,714.451',
'113.048,589.682,130.840,626.674', '464.160,633.570,481.952,670.562', '464.160,501.904,481.952,538.896'}

# sort by y0 decreasing, then x0 increasing
def _pos_sort(p):
    x0,y0,_,_ = map(float,p.split(','))
    return 100000000*(-y0)+x0

# build mapping of position to cell row,col coordinate
POS_MAP: Dict[str,Tuple[int,int]] = dict()
POS_MAP2: Dict[str,Tuple[int,int]] = dict()
_pos_tmp = sorted(POSITIONS, key=_pos_sort)
_pos_tmp2 = sorted(POSITIONS2, key=_pos_sort)

for r in range(9):
    for c in range(9):
        POS_MAP[_pos_tmp[9*r+c]] = (r,c)
        POS_MAP2[_pos_tmp2[9*r+c]] = (r,c)

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

def allowed_digits(puzzle: List[List[int]], r: int, c: int) -> List[bool]:
    br,bc = (r//3)*3, (c//3)*3 # upper left of block
    digits = [True]*10
    for i in range(9):
        digits[puzzle[r][i]] = False # row
        digits[puzzle[i][c]] = False # col
        digits[puzzle[br+(i//3)][bc+(i%3)]] = False # block
    return digits

def first_empty_cell(puzzle: List[List[int]]) -> Union[Tuple[int,int],None]:
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0:
                return r,c

def solved(puzzle: List[List[int]]) -> bool:
    digits = set(range(1,10))
    for i in range(9):
        if set(puzzle[i]) != digits: return False
        if set(puzzle[j][i] for j in range(9)) != digits: return False
        br,bc = divmod(i,3)
        if set(puzzle[3*br+j][3*bc+k] for j in range(3) for k in range(3)) != digits: return False
    return True

# constraint propagation
def propagate(allowed: List[List[List[bool]]], r: int, c: int, n: int):
    for i in range(9):
        allowed[r][i][n] = False
        allowed[i][c][n] = False
        br,bc = 3*(r//3),3*(c//3)
        dr,dc = divmod(i,3)
        allowed[br+dr][bc+dc][n] = False

# improved sudoku solver because it is too slow on the difficult puzzles
def solve_recur(puzzle: List[List[int]]) -> List[List[List[int]]]:
    allowed = [[allowed_digits(puzzle,r,c) for c in range(9)] for r in range(9)]
    while True: # try solving techniques
        changed = False
        for r in range(9): # cell with 1 possibility
            for c in range(9):
                if puzzle[r][c] != 0:
                    continue
                digits = allowed[r][c]
                i = 1 # find first true
                while i < 10 and not digits[i]: i += 1
                if i < 10 and not any(digits[i+1:]):
                    puzzle[r][c] = i
                    propagate(allowed,r,c,i)
                    changed = True
                if i == 10: return [] # impossible to solve
        for i in range(9): # row/col/block with 1 location for a number
            br,bc = divmod(i,3)
            for n in range(1,10): # digit
                # n in row i
                if n not in puzzle[i]:
                    pos = []
                    for c,digits in enumerate(allowed[i]):
                        if digits[n]: pos.append((i,c))
                    if len(pos) == 0:
                        return [] # impossible
                    if len(pos) == 1:
                        rr,cc = pos[0]
                        puzzle[rr][cc] = n
                        propagate(allowed,rr,cc,n)
                        changed = True
                # n in col i
                if n not in [puzzle[r][i] for r in range(9)]:
                    pos = []
                    for r in range(9):
                        if allowed[r][i][n]: pos.append((r,i))
                    if len(pos) == 0:
                        return [] # impossible
                    if len(pos) == 1:
                        rr,cc = pos[0]
                        puzzle[rr][cc] = n
                        propagate(allowed,rr,cc,n)
                        changed = True
                # n in block br,bc
                if n not in [puzzle[r][c] for r in range(3*br,3*br+3) for c in range(3*bc,3*bc+3)]:
                    pos = []
                    for dr in range(3):
                        for dc in range(3):
                            if allowed[3*br+dr][3*bc+dc][n]:
                                pos.append((3*br+dr,3*bc+dc))
                    if len(pos) == 0:
                        return [] # impossible
                    if len(pos) == 1:
                        rr,cc = pos[0]
                        puzzle[rr][cc] = n
                        propagate(allowed,rr,cc,n)
                        changed = True
        if not changed:
            break
    fec = first_empty_cell(puzzle)
    if fec is None: # filled
        assert solved(puzzle), '\n'+'\n'.join(str(row) for row in puzzle)
        return [[row[:] for row in puzzle]]
    # take a guess
    r,c = fec
    assert puzzle[r][c] == 0
    digits = allowed_digits(puzzle,r,c)
    solns = []
    for d in range(1,10):
        if not digits[d]:
            continue
        puzzle_copy = [row[:] for row in puzzle]
        puzzle_copy[r][c] = d
        solns += solve_recur(puzzle_copy)
        if len(solns) > 1: break # error if >1 solution
    return [] if len(solns) > 1 else solns
    # OLD BRUTE FORCE CODE
    # if pos == 81:
    #     return [[row[:] for row in puzzle]]
    # r,c = divmod(pos,9)
    # if puzzle[r][c] != 0:
    #     return solve_recur(puzzle,pos+1)
    # digits = allowed_digits(puzzle,r,c)
    # solns = []
    # for d in range(1,10): # try digits
    #     if not digits[d]:
    #         continue
    #     puzzle[r][c] = d
    #     solns += solve_recur(puzzle,pos+1)
    #     if len(solns) > 1: # error if multiple solutions
    #         break
    # puzzle[r][c] = 0 # backtrack
    # return [] if len(solns) > 1 else solns

def make_puzzle(pos_map: Dict[str,Tuple[int,int]], page_items: Dict[str,str]) -> List[List[int]]:
    puzzle = [[0]*9 for _ in range(9)]
    for pos,digit in page_items.items():
        digit = int(digit)
        r,c = pos_map[pos]
        assert puzzle[r][c] == 0
        assert 1 <= digit <= 9
        puzzle[r][c] = digit
    puzzle_copy = [row[:] for row in puzzle]
    solns = solve_recur(puzzle_copy)
    assert len(solns) == 1
    return puzzle

# difficulty(7 levels), vol(1..20 currently), book(1..100)
def _files_sort(file: str) -> int:
    match = FNAME_RE.fullmatch(file)
    assert match
    dif,vol,book = match.groups()
    vol = 1 if vol == '' else int(vol)
    book = int(book)
    diffs = ['EZ','NO','IM','CH','TF','ST','IN']
    return diffs.index(dif)*1000000 + vol*1000 + book

files = sorted(os.listdir(INPUT_DIR), key=_files_sort)
#_p=set() # for collecting possible positions

print('DIFFICULTY,VOLUME,BOOK,NUMBER,PUZZLE') # header row

for file in tqdm.tqdm(files):
    match = FNAME_RE.fullmatch(file)
    assert match
    dif,vol,book = match.groups()
    vol = 1 if vol == '' else int(vol)
    book = int(book)
    tqdm.tqdm.write('parsing: '+file+' (dif = %s, vol = %d, book = %d)'%(dif,vol,book), sys.stderr)
    file = INPUT_DIR+'/'+file
    file_data = bz2.open(file,'rt').read()
    assert file_data.splitlines()[-1] == '</pages>', file_data.splitlines()[-1] # check if file is complete
    xml = bs4.BeautifulSoup(file_data,features='xml')
    text = extract_text(xml)
    for p,page in enumerate(text):
        #_p|=set(page.keys())
        #continue
        #tqdm.tqdm.write('- puzzle '+str(p+1), sys.stderr)
        try:
            puzzle = make_puzzle(POS_MAP,page)
        except:
            puzzle = make_puzzle(POS_MAP2,page)
        # convert to string of 81 chars
        puzzle_str = ''.join(''.join(map(str,row)) for row in puzzle)
        #puzzle_json = json.dumps({
        #    'dif': dif,
        #    'vol': 1 if vol == '' else int(vol),
        #    'book': int(book),
        #    'num': p+1,
        #    'puzzle': puzzle_str
        #}, separators=(',',':'))
        #print(puzzle_json)
        print('%s,%d,%d,%d,%s'%(dif,vol,book,p+1,puzzle_str))

#print(_p)
#print(_p.__len__())
