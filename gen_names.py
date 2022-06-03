# filename generator for krazydad scraping

# https://krazydad.com/sudoku/sfiles/*
def sudokuComplete():
    for dif in ['EZ','NO','IM','CH','TF','ST','IN']:
        for vol in range(1,21):
            print('KD_Sudoku_%s%s_4up.pdf'%(dif,''if vol==1 else str(vol)))

# https://krazydad.com/sudoku/sfiles/*
def sudoku1PP():
    for dif in ['EZ','NO','IM','CH','TF','ST','IN']:
        for vol in range(1,21):
            for book in range(1,101):
                print('KD_Sudoku_%s%s_8_v%d.pdf'%(dif,''if vol==1 else str(vol),
                                                  book))

# https://krazydad.com/sudoku/sfiles/*
def sudoku4PP():
    for dif in ['EZ','NO','IM','CH','TF','ST','IN']:
        for vol in range(1,21):
            for book in range(1,101):
                print('KD_Sudoku_%s%s_4up_v%d.pdf'%(dif,
                                                ''if vol==1 else str(vol),book))

# https://krazydad.com/mazes/sfiles/*
def mazes():
    for dif in ['EZ','IM','CH','TF','ST']:
        for book in range(1,51):
            print('KD_Mazes_%s_v%d.pdf'%(dif,book))
    for dif in ['EasyDinosaurMazes','DinosaurMazes','AnimalMazes']:
        for book in range(1,51):
            print('KD_%s_v%d.pdf'%(dif,book))

# https://krazydad.com/inkies/sfiles/*
def inkies4PP():
    for dif in ['3KX','3E','3X','4KX','4E','4M','4H','4X','4NOP','5KX','5E',
                '5M','5H','5X','5NOP','6KX','6E','6M','6H','6X','6NOP','7H',
                '7X','7NOP','8H','8X','9H','9X']:
        for vol in range(1,21):
            for book in range(1,101):
                print('INKY_%s%s_b%03d_4pp.pdf'%(''if vol==1 else 'v%d_'%vol,
                                                 dif,book))

# https://krazydad.com/inkies/sfiles/*
def inkies1PP():
    for dif in ['6KX','6E','6M','6H','6X','6NOP','7H','7X','7NOP','8H','8X',
                '9H','9X']:
        for vol in range(1,21):
            for book in range(1,101):
                print('INKY_%s%s_b%03d_1pp.pdf'%(''if vol==1 else 'v%d_'%vol,
                                                 dif,book))

# https://krazydad.com/killersudoku/sfiles/*
def killerSudoku1PP():
    for dif in ['IM','CH','TF','ST','IN']:
        volrange = range(1,25)
        for vol in volrange:
            for book in range(1,101):
                print('KD_Killer_%s%d_8_v%d.pdf'%(dif,vol,book))

# https://krazydad.com/killersudoku/sfiles/*
def killerSudoku4PP():
    for dif in ['IM','CH','TF','ST','IN']:
        volrange = range(1,25)
        for vol in volrange:
            for book in range(1,101):
                print('KD_Killer_%s%d_4up_v%d.pdf'%(dif,vol,book))

# https://krazydad.com/killersudoku/sfiles/*
def killerSudokuComplete():
    for dif in ['IM','CH','TF','ST','IN']:
        volrange = range(1,19) if dif == 'IN' else range(1,21)
        for vol in volrange:
            print('KD_KillerSudoku_%s%d_4up.pdf'%(dif,vol))

# https://krazydad.com/jigsawsudoku/sfiles/*
def jigsawSudokuComplete():
    for dif in ['IM','CH','TF','ST']:
        for vol in range(1,16):
            print('KD_Jigsaw_%s%d_4up.pdf'%(dif,vol))

# https://krazydad.com/jigsawsudoku/sfiles/*
def jigsawSudoku1PP():
    for dif in ['IM','CH','TF','ST']:
        for vol in range(1,16):
            for book in range(1,101):
                print('KD_Jigsaw_%s%d_8_v%d.pdf'%(dif,vol,book))

# https://krazydad.com/jigsawsudoku/sfiles/*
def jigsawSudoku4PP():
    for dif in ['IM','CH','TF','ST']:
        for vol in range(1,16):
            for book in range(1,101):
                print('KD_Jigsaw_%s%d_4up_v%d.pdf'%(dif,vol,book))

# https://krazydad.com/kakuro/books/*
def kakuroKrazydad():
    for dif in ['5x5','6x6','8x8','10x10','10x10D','10x10I','12x12','15x15',
                '11x17','13x17','13x17D','13x17I']:
        volrange = range(1,9) if dif[-1] in 'DI' else range(1,16)
        for vol in volrange:
            for book in range(1,101):
                print('KD_Kakuro_%s%s_s2_b%03d.pdf'%(dif,
                                        ''if vol==1 else'_v%d'%vol,book))

# https://krazydad.com/kakuro/books/*
def kakuroCommon():
    for dif in ['5x5','6x6','8x8','10x10','10x10D','10x10I','12x12','15x15',
                '11x17','13x17','13x17D','13x17I']:
        volrange = range(1,9) if dif[-1] in 'DI' else range(1,16)
        for vol in volrange:
            for book in range(1,101):
                print('KD_Kakuro_%s%s_s0_b%03d.pdf'%(dif,
                                        ''if vol==1 else'_v%d'%vol,book))

# https://krazydad.com/kakuro/books/*
def kakuroLarge():
    for dif in ['5x5','6x6']:
        for vol in range(1,16):
            for book in range(1,101):
                print('KD_Kakuro_%s%s_s2L_b%03d.pdf'%(dif,
                                        ''if vol==1 else'_v%d'%vol,book))

# https://krazydad.com/suguru/sfiles/*
def suguru():
    for dif in ['6x6','8x8']:
        for vol in range(1,16):
            for book in range(1,101):
                print('SUG_%s_v%d_4pp_b%d.pdf'%(dif,vol,book))
    for dif in ['12x10','15x10','15x10n6']:
        for vol in range(1,16):
            for book in range(1,101):
                print('SUG_%s_v%d_2pp_b%d.pdf'%(dif,vol,book))

# https://krazydad.com/starbattle/sfiles/*
def starBattle():
    for dif in ['8x8','10x10','14x14']:
        volrange = range(1,6) if dif == '14x14' else range(1,9)
        for vol in volrange:
            for book in range(1,101):
                print('STAR_%s_v%d_b%d.pdf'%(dif,vol,book))

# https://krazydad.com/kidoku/books/*
def kidoku():
    for dif in ['4x4','6x6','8x8']:
        for book in range(1,101):
            print('KD_Kidoku_%s_v%d.pdf'%(dif,book))

# https://krazydad.com/kidoku/books/*
def kidokuComplete():
    for dif in ['4x4','6x6','8x8']:
        print('KID_%s_4up.pdf'%dif)

# https://krazydad.com/slitherlink/sfiles/*
def slitherlink():
    for dif in ['d0_07x07','d0_10x10','d0_20x20','d1_07x07','d1_10x10',
                'd1_20x20','d2_07x07','d2_10x10','d2_20x20']:
        for vol in range(1,3):
            for book in range(1,401):
                print('sl_%s%s_b%03d.pdf'%(''if vol==1 else'v%d_'%vol,dif,book))
    for typ in ['variety','penrose','altair','laves','snowflake','hexagons',
                'cairo','snubsquare','rhomboid','floret','septistar',
                'easy_penrose']:
        for book in range(1,101):
            print('sl_%s_b%03d.pdf'%(typ,book))

# https://krazydad.com/skyscraper/sfiles/*
def skyscrapers():
    for dif in ['5x','6x','sudsky','krazytown']:
        for vol in range(1,3):
            for book in range(1,101):
                print('KD_SKY_%s_V%d_B%d.pdf'%(dif,vol,book))

# https://krazydad.com/sandwich/sfiles/*
def sandwichSudoku():
    for typ in ['reg','blt','dagwood','sliders']:
        for vol in range(1,3):
            for book in range(1,101):
                print('KD_SAND_%s_V%d_B%d.pdf'%(typ,vol,book))

# https://krazydad.com/xsudoku/sfiles/*
def xSudoku():
    for typ in ['reg','jigx','centerdot','prisoner','cellblock']:
        for vol in range(1,3):
            for book in range(1,101):
                print('KD_XSUD_%s_V%d_B%d.pdf'%(typ,vol,book))

# https://krazydad.com/battleships/sfiles/*
def battleship():
    for dif in ['6x6','8x8','10x10','12x12','12x12R','15x15R']:
        pp = 4 if dif in ['6x6','8x8'] else 2 # per page
        for vol in range(1,6):
            for book in range(1,101):
                print('BSHIPS_%s_v%d_%dpp_b%d.pdf'%(dif,vol,pp,book))

# https://krazydad.com/consecutive/sfiles/*
def consecutiveSudoku():
    for typ in ['reg','jigcon','kravitz']:
        for vol in range(1,3):
            for book in range(1,101):
                print('KD_CON_%s_V%d_B%d.pdf'%(typ,vol,book))

# https://krazydad.com/bridges/books/*
def bridges():
    for typ in ['SM','MD','LG','XL']:
        for vol in range(1,6):
            for book in range(1,101):
                print('BR_%s%s_b%d.pdf'%(typ,''if vol==1 else str(vol),book))

# https://krazydad.com/futoshiki/sfiles/*
def futoshiki():
    for typ in ['4x','5x','6x','7x','8x','9x']:
        for vol in range(1,9):
            for book in range(1,101):
                print('FUT_%s_v%d_b%d.pdf'%(typ,vol,book))

# https://krazydad.com/samurai/sfiles/*
def samuraiSudoku():
    for typ in ['SAM2','SAM5']:
        for vol in range(1,10):
            for book in range(1,101):
                print('%s_v%d_b%d.pdf'%(typ,vol,book))

# https://krazydad.com/hexsudoku/sfiles/*
def hexSudokuHex():
    for dif in ['IMH','CHH','TFH','STH']:
        for vol in range(1,8):
            for book in range(1,101):
                print('KD_HexSudoku_%s%s_8_v%d.pdf'%(dif,
                                ''if vol==1 else str(vol),book))

# https://krazydad.com/hexsudoku/sfiles/*
def hexSudokuDec():
    for dif in ['IMHd','CHHd','TFHd','STHd']:
        for vol in range(1,8):
            for book in range(1,101):
                print('KD_HexSudoku_%s%s_8_v%d.pdf'%(dif,
                                ''if vol==1 else str(vol),book))

# https://krazydad.com/ripple/sfiles/*
def rippleEffect():
    for dif in ['EZ_7x7','CH_8x8','TF_8x8','ST_10x10']:
        for vol in range(1,3):
            for book in range(1,101):
                print('RIP_%s_v%d_4pp_b%d.pdf'%(dif,vol,book))

# https://krazydad.com/area51/sfiles/*
def area51():
    for dif in ['8x10_easy','8x10_hard','19x22_easy','19x22_hard']:
        for vol in range(1,2):
            for book in range(1,101):
                print('AREA51_%s_v%d_b%03d.pdf'%(dif,vol,book))

# https://krazydad.com/masyu/sfiles/*
def masyu():
    for dif in ['6E','6M','6H','8E','8M','8H','10E','10M','10H','1012E','1012M',
                '1012H','1510E','1510M','1510H','1315E','1315M','1315H']:
        for vol in range(1,3):
            for book in range(1,101):
                print('MASYU_%s%s_b%03d.pdf'%(''if vol==1 else'v%d_'%vol,
                                dif,book))

# https://krazydad.com/binox/sfiles/*
def binox():
    for dif in ['6x6_EZ','6x6_NV','6x6_CH','6x6_TF','8x8_EZ','8x8_NV','8x8_CH',
                '8x8_TF','10x10_EZ','10x10_NV','10x10_CH','10x10_TF','12x12_NV',
                '12x12_CH','12x12_TF','14x14_NV','14x14_CH','14x14_TF']:
        pp = 2 if dif.startswith('12x12') or dif.startswith('14x14') else 4
        for vol in range(1,3):
            for book in range(1,101):
                print('BINOX_%s_v%d_%dpp_b%d.pdf'%(dif,vol,pp,book))

# https://krazydad.com/crossfigures/*
def crossFigures():
    print('ydir_crossfigures_1_20.pdf')
    print('ydir_crossfigures_21_40.pdf')
    print('ydir_crossfigures_41_60.pdf')
    print('ydir_crossfigures_61_80.pdf')

# https://krazydad.com/jigoku/books/*
def jigoku():
    for dif in ['CH','TF','ST','IN']:
        for book in range(1,101):
            print('KD_Jigoku_%s_8_v%d.pdf'%(dif,book))

# https://krazydad.com/jigoku/books/*
def jigokuComplete():
    for dif in ['CH','TF','ST','IN']:
        print('KD_Jigoku_%s_4up.pdf'%dif)

# https://krazydad.com/kinkies/sfiles/*
def kryptoInkies():
    for typ in ['5x','6x','7x','8x']:
        for vol in range(1,6):
            for book in range(1,101):
                print('KINKIES_%s_v%d_b%d.pdf'%(typ,vol,book))

# https://krazydad.com/krypto/books/*
def kryptoKakuro():
    for vol in range(1,6):
        for book in range(1,201):
            print('KD_KryptoKakuro_%sB%03d.pdf'%(''if vol==1 else'v%d_'%vol,
                                book))

# http://krazydad.com/galaxies/books/*
def galaxies():
    for typ in ['d7','d10','d11','d21']:
        for vol in range(1,6):
            for book in range(1,101):
                print('GAL%s_%s_b%d.pdf'%(''if vol==1 else str(vol),typ,book))

# https://krazydad.com/corral/sfiles/*
def corral():
    for typ in ['8x10','19x22']:
        for vol in range(1,2):
            for book in range(1,101):
                print('CORRAL_%s_v%d_b%03d.pdf'%(typ,vol,book))

# https://krazydad.com/haunted/sfiles/*
def haunted():
    for vol in range(1,3):
        for book in range(1,101):
            print('KD_Haunted_V%d_N%d.pdf'%(vol,book))

# command examples
# for f in $(python3 ../gen_names.py); do proxychains wget -nc -e robots=off -U "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0" $BASE_URL/$f; done
# python3 ../gen_names.py | parallel -j1 proxychains wget -nc -e robots=off -U "\"Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0\"" "\"$BASE_URL/{}\""

if __name__ == '__main__': pass
