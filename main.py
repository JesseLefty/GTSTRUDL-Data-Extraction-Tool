# File Object
import extract_member_forces as emf
from tabulate import tabulate


member_forces = emf.member_force_final()
print(f' {member_forces.nbytes / 1000} KB')


with open('member_forces.txt', 'w') as w:
    table_output = tabulate(member_forces, colalign=('left', 'center'))
    w.write(table_output)