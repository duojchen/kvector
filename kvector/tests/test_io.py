import os
import pandas as pd
import pandas.util.testing as pdt
import pytest
import six


'''
Note: The lines that end with:
# noqa
are like the so the linter/syntax checker doesn't complain that the lines are
>80 columns (PEP8 standard)
'''


@pytest.fixture
def motifs_filename(data_folder):
    return os.path.join(data_folder, 'example_rbps.motif')


def test_read_motifs(motifs_filename):
    import kvector

    test = kvector.read_motifs(motifs_filename)

    s = '''M001_0.6_A1CF_ENSG00000148584_Homo_sapiens	M001_0.6_A1CF_ENSG00000148584_Homo_sapiens	5.0,",A,C,G,T# noqa
0,0.39532879396435,0.10551388868612599,0.10551388868612599,0.39364342774540506
1,0.00770456803068082,0.00770456803068082,0.00770456803068082,0.976886297348457
2,0.976886297348457,0.00770456803068082,0.00770456803068082,0.00770456803068082
3,0.976886297348457,0.00770456803068082,0.00770456803068082,0.00770456803068082
4,0.00770456803068082,0.00770456803068082,0.00770456803068082,0.976886297348457
5,0.00770456803068082,0.00770456803068082,0.00770456803068082,0.976886297348457
6,0.321131137484576,0.14380369811499302,0.478370946765367,0.0566942181612342
"
M002_0.6_ANKRD17_ENSG00000132466_Homo_sapiens	M002_0.6_ANKRD17_ENSG00000132466_Homo_sapiens	5.0,",A,C,G,T# noqa
0,0.773202708628553,0.0755990967724702,0.0755990967724702,0.0755990967724702
1,0.00430461221593073,0.00430461221593073,0.9870861613459828,0.00430461221593073# noqa
2,0.9870861613459828,0.00430461221593073,0.00430461221593073,0.00430461221593073# noqa
3,0.00430461221593073,0.9870861613459828,0.00430461221593073,0.00430461221593073# noqa
4,0.00430461221593073,0.00430461221593073,0.9870861613459828,0.00430461221593073# noqa
5,0.22880975523660801,0.10208869663005,0.00430461221593073,0.664796933911185
6,0.427754153606094,0.0793093155884373,0.0997300686202917,0.393206460178951
"
M003_0.6_FBgn0262475_FBgn0262475_Drosophila_melanogaster	M003_0.6_FBgn0262475_FBgn0262475_Drosophila_melanogaster	5.0,",A,C,G,T# noqa
0,0.0983441407394978,0.0983441407394978,0.0983441407394978,0.704967578595223
1,0.00457897434436391,0.00457897434436391,0.7118873003534859,0.278954749988551
2,0.00457897434436391,0.00457897434436391,0.18604575865396106,0.8047962916880749# noqa
3,0.00457897434436391,0.00457897434436391,0.7346313744116741,0.256210675930362
4,0.00457897434436391,0.00457897434436391,0.00457897434436391,0.9862630759976719# noqa
5,0.00457897434436391,0.00457897434436391,0.822768953386897,0.16807309695514
6,0.0285430063447848,0.0285430063447848,0.11605126951013998,0.8268627169511971
"
M004_0.6_BRUNOL4_ENSG00000101489_Homo_sapiens	M004_0.6_BRUNOL4_ENSG00000101489_Homo_sapiens	5.0,",A,C,G,T# noqa
0,0.0850634504936057,0.0850634504936057,0.175951658141761,0.6539214362304301
1,0.0130464984118041,0.0130464984118041,0.776576805287808,0.197330201099004
2,0.0130464984118041,0.0130464984118041,0.0130464984118041,0.9608605079750091
3,0.0130464984118041,0.0130464984118041,0.764576198088384,0.20933080829842998
4,0.0130464984118041,0.0130464984118041,0.104633577159811,0.8692734292270029
5,0.0130464984118041,0.0130464984118041,0.6667990251158571,0.30710798127095695
6,0.0831008331277267,0.0831008331277267,0.26454785801693803,0.56925047512411
"'''
    true = pd.read_csv(six.StringIO(s), index_col=0, header=None,
                       squeeze=True, comment='#')
    true = true.map(lambda x: pd.read_csv(six.StringIO(x), index_col=0,
                                          comment='#'))
    true.name = None
    true.index.name = None
    pdt.assert_index_equal(test.index, true.index)

    zipped = zip(test.iteritems(), true.iteritems())
    for (index1, df1), (index2, df2) in zipped:
        assert index1 == index2
        pdt.assert_frame_equal(df1, df2)


def test_motifs_to_kmer_vectors(motifs_filename):
    import kvector

    motifs = kvector.read_motifs(motifs_filename)
    test = kvector.motifs_to_kmer_vectors(motifs, 2)

    s = ''',M001_0.6_A1CF_ENSG00000148584_Homo_sapiens	M001_0.6_A1CF_ENSG00000148584_Homo_sapiens	5.0,M002_0.6_ANKRD17_ENSG00000132466_Homo_sapiens	M002_0.6_ANKRD17_ENSG00000132466_Homo_sapiens	5.0,M003_0.6_FBgn0262475_FBgn0262475_Drosophila_melanogaster	M003_0.6_FBgn0262475_FBgn0262475_Drosophila_melanogaster	5.0,M004_0.6_BRUNOL4_ENSG00000101489_Homo_sapiens	M004_0.6_BRUNOL4_ENSG00000101489_Homo_sapiens	5.0# noqa
AA,0.3891860440855699,0.3048813640579511,0.014389740877326808,0.024885772311614447# noqa
AC,0.21287846925180864,0.26528420600593317,0.014389740877326808,0.024885772311614447# noqa
AG,0.24075907330600646,0.3407357241515821,0.22476688692681998,0.22837299205276904# noqa
AT,0.4479147782517728,0.2564361920677329,0.2868666349976929,0.2719541121289282
CA,0.20350451375942188,0.23618764151939767,0.014389740877326808,0.024885772311614447# noqa
CC,0.027196938925660597,0.19659048346737976,0.014389740877326808,0.024885772311614447# noqa
CG,0.05507754297985843,0.2720420016130287,0.22476688692681998,0.22837299205276904# noqa
CT,0.2622332479256248,0.1877424695291795,0.2868666349976929,0.2719541121289282
GA,0.20350451375942188,0.3099374302457254,0.21747453166304034,0.2208264239493477# noqa
GC,0.027196938925660597,0.27034027219370754,0.21747453166304034,0.2208264239493477# noqa
GG,0.05507754297985843,0.3457917903393564,0.42785167771253346,0.42431364369050223# noqa
GT,0.2622332479256248,0.2614922582555072,0.4899514257834065,0.4678947637666615
TA,0.46981074101047254,0.20118153219865456,0.27089194560180224,0.2788464741072983# noqa
TC,0.29350316617671124,0.1615843741466367,0.27089194560180224,0.2788464741072983# noqa
TG,0.3213837702309091,0.2370358922922856,0.4812690916512954,0.482333693848453
TT,0.5285394751766753,0.15273636020843642,0.5433688397221682,0.5259148139246123
'''
    true = pd.read_csv(six.StringIO(s), index_col=0, comment='#')

    pdt.assert_frame_equal(test, true)
