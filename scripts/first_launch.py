import ansys.fluent.core as pyfluent

solver = pyfluent.launch_fluent(mode="solver", show_gui=True)
print("Connected!")

input("Fluent is running. Press Enter in this terminal to close it...")

solver.exit()