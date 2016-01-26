
import mocup

for R in range(1,5):
    for Z in range(1,6):
        node_mat = mocup.material()
        print dir(node_mat)

        for B in range(1,9):
            mat_loc = 'moi_files/moi.%d%d%d00.eq.pch' % (R,Z,B)
            mat = mocup.material()
            mat.import_ocf(mat_loc)
            node_mat = node_mat + mat

        mat_loc = 'eq_files/node.%d%d.eq' % (R,Z)
        node_mat.make_ocf(mat_loc,lib=node_mat.lib)
