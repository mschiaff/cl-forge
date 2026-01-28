use pyo3::prelude::*;

#[pymodule]
fn rs_cl_forge(py: Python<'_>, module: &Bound<'_, PyModule>) -> PyResult<()> {
    let cmf_mod = PyModule::new(py, "rs_cmf")?;
    cmf::rs_cmf(&cmf_mod)?;
    module.add_submodule(&cmf_mod)?;

    let verify_mod = PyModule::new(py, "rs_verify")?;
    verify::rs_verify(&verify_mod)?;
    module.add_submodule(&verify_mod)?;

    let market_mod = PyModule::new(py, "rs_market")?;
    market::rs_market(&market_mod)?;
    module.add_submodule(&market_mod)?;

    let base_mod = PyModule::new(py, "rs_base")?;
    base::rs_base(&base_mod)?;
    module.add_submodule(&base_mod)?;

    let sys_mod = py.import("sys")?.getattr("modules")?;
    sys_mod.set_item("cl_forge.core.impl.rs_cl_forge.rs_cmf", cmf_mod)?;
    sys_mod.set_item("cl_forge.core.impl.rs_cl_forge.rs_verify", verify_mod)?;
    sys_mod.set_item("cl_forge.core.impl.rs_cl_forge.rs_market", market_mod)?;
    sys_mod.set_item("cl_forge.core.impl.rs_cl_forge.rs_base", base_mod)?;

    Ok(())
}