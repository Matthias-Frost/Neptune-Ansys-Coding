from pathlib import Path
import csv
import ansys.fluent.core as pyfluent

MODEL = Path(__file__).resolve().parent / "Models" / "mixing_elbow"

solver = pyfluent.launch_fluent(
    mode="solver", ui_mode="gui", precision="double", processor_count=2
)
solver.file.read_case(file_name=str(MODEL / "mixing_elbow.msh.h5"))

solver.setup.models.energy.enabled = True

solver.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")
solver.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"

cold_inlet = solver.setup.boundary_conditions.velocity_inlet["cold-inlet"]
hot_inlet = solver.setup.boundary_conditions.velocity_inlet["hot-inlet"]

cold_inlet.vmag = 0.4
cold_inlet.ke_spec = "Intensity and Hydraulic Diameter"
cold_inlet.turb_intensity = 0.05
cold_inlet.turb_hydraulic_diam = "4 [in]"
cold_inlet.t = 293.15

hot_inlet.vmag = 1.2
hot_inlet.ke_spec = "Intensity and Hydraulic Diameter"
hot_inlet.turb_intensity = 0.05
hot_inlet.turb_hydraulic_diam = "1 [in]"
hot_inlet.t = 313.15

outlet = solver.setup.boundary_conditions.pressure_outlet["outlet"]

outlet.turb_intensity = 0.05
outlet.turb_viscosity_ratio = 4

solver.solution.report_definitions.surface["outlet_temp"] = {}
outlet_temp = solver.solution.report_definitions.surface["outlet_temp"]
outlet_temp.report_type = "surface-massavg"
outlet_temp.field = "temperature"
outlet_temp.surface_names = ["outlet"]

solver.solution.monitor.report_files["outlet_temp_file"] = {}
solver.solution.monitor.report_files["outlet_temp_file"].report_defs = ["outlet_temp"]

results = []
for v in [0.6, 1.2, 1.8]:
    out = MODEL / f"outlet_temp_v{v}.out"
    out.unlink(missing_ok=True)

    hot_inlet.vmag = v
    solver.solution.monitor.report_files["outlet_temp_file"].file_name = str(out)

    solver.solution.initialization.hybrid_initialize()
    solver.solution.run_calculation.iterate(iter_count=150)

    rows = [line.split() for line in out.read_text().splitlines()]
    data = [r for r in rows if r and r[0].isdigit()]
    iteration = int(data[-1][0])
    temp = float(data[-1][-1])

    predicted = 293.15 + 20 * v / (v + 6.4)
    results.append((v, iteration, temp, predicted))
    print(f"v={v}: {temp:.3f} K at iteration {iteration} (hand estimate {predicted:.2f} K)")

with open(MODEL / "sweep_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["hot_velocity_m_s", "iterations", "outlet_temp_K", "hand_estimate_K"])
    w.writerows(results)


solver.exit()