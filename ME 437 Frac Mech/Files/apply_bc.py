from abaqus import *
from abaqusConstants import *
import regionToolset
import math

model = mdb.models['Model-1']
assembly = model.rootAssembly

# CREATE STEP FIRST
model.StaticStep(
    name='Step-1',
    previous='Initial'
)

# Node set on outer boundary
nodeSet = assembly.sets['Set-1']
nodes = nodeSet.nodes

A = 8.41e-5

for i in range(len(nodes)):

    node = nodes[i]

    x = node.coordinates[0]
    y = node.coordinates[1]

    # Polar coordinates
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)

    # Displacement equations
    u = A * math.sqrt(r) * math.cos(theta/2.0) * (2.0 - math.cos(theta))

    v = A * math.sqrt(r) * math.sin(theta/2.0) * (2.0 - math.cos(theta))

    # Create region
    region = regionToolset.Region(nodes=nodes[i:i+1])

    model.DisplacementBC(
        name='BC-%d' % i,
        createStepName='Step-1',
        region=region,
        u1=u,
        u2=v,
        ur3=UNSET
    )

print('Boundary conditions created successfully')