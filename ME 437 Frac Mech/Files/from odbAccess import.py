from odbAccess import *
from abaqusConstants import *

# -------------------------------------------------
# USER INPUTS
# -------------------------------------------------

odb_name = 'Job-1.odb'
step_name = 'Step-1'
set_name = 'SET-1'

output_file = r'D:\Documents\Frac Mech\nodal_stress_average.csv'

# -------------------------------------------------
# OPEN ODB
# -------------------------------------------------

odb = openOdb(odb_name)

frame = odb.steps[step_name].frames[-1]

stress = frame.fieldOutputs['S']

node_set = odb.rootAssembly.nodeSets[set_name]

# ELEMENT_NODAL gives repeated nodes
subset = stress.getSubset(
    region=node_set,
    position=ELEMENT_NODAL
)

# -------------------------------------------------
# AVERAGE STRESSES AT EACH NODE
# -------------------------------------------------

stress_data = {}

for v in subset.values:

    node = v.nodeLabel

    s11 = v.data[0]
    s22 = v.data[1]

    if len(v.data) > 3:
        s12 = v.data[3]
    else:
        s12 = 0.0

    # Initialize
    if node not in stress_data:
        stress_data[node] = [0.0, 0.0, 0.0, 0]

    # Sum stresses
    stress_data[node][0] += s11
    stress_data[node][1] += s22
    stress_data[node][2] += s12

    # Counter
    stress_data[node][3] += 1

# -------------------------------------------------
# WRITE AVERAGED RESULTS
# -------------------------------------------------

with open(output_file, 'w') as f:

    f.write('Node_Label,S11,S22,S12\n')

    for node in sorted(stress_data.keys()):

        count = stress_data[node][3]

        avg_s11 = stress_data[node][0] / count
        avg_s22 = stress_data[node][1] / count
        avg_s12 = stress_data[node][2] / count

        f.write('%d,%e,%e,%e\n' % (
            node,
            avg_s11,
            avg_s22,
            avg_s12
        ))

odb.close()

print('DONE')
print(output_file)