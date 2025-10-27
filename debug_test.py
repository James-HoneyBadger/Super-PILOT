from Super_PILOT import SuperPILOTInterpreter

interp = SuperPILOTInterpreter()
program = """
U:X=5
U:Y=10
C:SUM=X+Y
"""
interp.run_program(program)
print("Variables:", interp.variables)
print("SUM =", interp.variables.get('SUM'))
print("Type:", type(interp.variables.get('SUM')))
