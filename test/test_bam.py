from MrBam.bam import get_reads
from helper import make_bam
from argparse import Namespace
from pysam import AlignmentFile

def test_get_reads_1(tmpdir):
    "it should get all but only the reads that covers the given position"

    make_bam(tmpdir.strpath, """
        r1 + ...........
        r1 -      ......*....
        r2 +   .........*.
        r2 -       .....*.......
        r3 +       ...........
        r3 -            ....*......
        r4 +       ...........
        r4 -            ...........
    """)

    o = Namespace(verbos=False)
    sam = AlignmentFile(tmpdir.join("test.bam").strpath)

    assert sum( 1 for _ in get_reads(o, sam, 'ref', '4') )  == 2
    assert sum( 1 for _ in get_reads(o, sam, 'ref', '12') ) == 7
    assert sum( 1 for _ in get_reads(o, sam, 'ref', '20') ) == 2

def test_get_reads_2(tmpdir):
    "it should read properties correctly"

    make_bam(tmpdir.strpath, """
        r1 + ...*.......
        r1 -   .*.........
    """)

    o = Namespace(verbos=False)
    sam = AlignmentFile(tmpdir.join("test.bam").strpath)

    r = next(get_reads(o, sam, 'ref', '4'))

    assert r[0] == "r1" # name
    assert r[3] == 0 # 0-based pos
    assert r[4] == 11 # length
    assert r[5] == 2 # mate pos
    assert r[6] == 13 # template length
    assert r[7] == False # is_reverse
    assert r[8] == True # paired and mapped
