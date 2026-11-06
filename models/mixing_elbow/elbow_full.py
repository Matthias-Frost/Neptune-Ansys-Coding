from pathlib import Path
import ansys.fluent.core as pyfluent

MODEL = Path(__file__).resolve().parent / "Models" / "mixing_elbow"
OUT = MODEL / "outlet_temp.out"
OUT.unlink(missing_ok=True)

solver = pyfluent.launch_fluent(
    mode="solver", ui_mode="gui", precision="double" , processor_count=2
)

solver.tui.file.read_case(str(MODEL / "mixing_elbow.msh.h5"))

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

rd = solver.solution.report_definitions                     # find the surface-type report collection

rd.surface["outlet_temp"] = {}
outlet_temp = rd.surface["outlet_temp"]
outlet_temp.report_type = "surface-massavg"
outlet_temp.field = "temperature"
outlet_temp.surface_names = ["outlet"]
outlet_temp.print_state()

mon = solver.solution.monitor
mon.report_files["outlet_temp_file"] = {}
rf = mon.report_files["outlet_temp_file"]
rf.print_state()
rf.report_defs = ["outlet_temp"]
rf.file_name = str(MODEL / "outlet_temp.out")
rf.print_state()

solver.solution.initialization.hybrid_initialize()
solver.solution.run_calculation.iterate(iter_count=150)

solver.file.write(
    file_type="case-data",
    file_name=str(MODEL / "mixing_elbow_result.cas.h5"),
)

rows = [l.split() for l in (MODEL / "outlet_temp.out").read_text().splitlines()]
data = [r for r in rows if r and r[0].isdigit()]
outlet_temp_K = float(data[-1][-1])
print(f"Outlet temperature at iteration {data[-1][0]}: {outlet_temp_K:.3f} K")

solver.exit()