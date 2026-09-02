use pyo3::prelude::*;


#[pymodule]
fn rs_cl_forge(py: Python<'_>, module: &Bound<'_, PyModule>) -> PyResult<()> {
    let verify_mod = PyModule::new(py, "rs_verify")?;
    verify::rs_verify(&verify_mod)?;
    module.add_submodule(&verify_mod)?;

    let sys_mod = py.import("sys")?.getattr("modules")?;
    sys_mod.set_item("cl_forge.core.impl.rs_cl_forge.rs_verify", verify_mod)?;

    Ok(())
}
