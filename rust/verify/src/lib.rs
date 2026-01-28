pub mod enums;
pub mod constants;
pub mod utils;
pub mod errors;

use pyo3::prelude::*;
use pyo3::create_exception;
use pyo3::types::{PyDict, PyList};
use pyo3::exceptions::PyException;

use crate::errors::PpuError;
use crate::errors::VerifierError;
use crate::errors::GenerateError;


create_exception!(
    rs_verify, PpuException, PyException,
    "Base class for all exceptions raised by the PPU."
);
create_exception!(
    rs_verify, UnknownFormat, PpuException,
    "Raised when the given PPU does not match any known format."
);
create_exception!(
    rs_verify, InvalidLength, PpuException,
    "Raised when PPU letters or digraphs are of invalid length."
);
create_exception!(
    rs_verify, UnknownLetter, PpuException,
    "Raised when the given PPU has letters out of the mapping."
);
create_exception!(
    rs_verify, EmptyLetter, PpuException,
    "Raised when internal mapping functions encounter an empty letter."
);
create_exception!(
    rs_verify, UnknownDigraph, PpuException,
    "Raised when the given PPU has digraphs out of the mapping."
);
create_exception!(
    rs_verify, EmptyDigraph, PpuException,
    "Raised when internal mapping functions encounter an empty digraph."
);

create_exception!(
    rs_verify, VerifierException, PyException,
    "Base class for all exceptions raised by the verifier."
);
create_exception!(
    rs_verify, EmptyVerifier, VerifierException,
    "Raised when the given verifier is empty on RUT validation."
);
create_exception!(
    rs_verify, InvalidVerifier, VerifierException,
    "Raised when the given verifier is invalid on RUT validation."
);
create_exception!(
    rs_verify, UnexpectedComputation, VerifierException,
    "Raised when the verifier computation fails."
);

create_exception!(
    rs_verify, GenerateException, PyException,
    "Base class for all exceptions raised by the RUT generator."
);
create_exception!(
    rs_verify, InvalidRange, GenerateException,
    "Raised when the generator given lower bound is greater than upper bound."
);
create_exception!(
    rs_verify, InvalidInput, GenerateException,
    "Raised when generator's given parameters are invalid."
);
create_exception!(
    rs_verify, InsufficientRange, GenerateException,
    "Raised when the requested amount of RUTs is greater than the available range."
);
create_exception!(
    rs_verify, UnexpectedGeneration, GenerateException,
    "Raised to support unidentified errors during RUT generation."
);

impl From<PpuError> for PyErr {
    fn from(err: PpuError) -> PyErr {
        match err {
            PpuError::UnknownFormat { .. } => UnknownFormat::new_err(err.to_string()),
            PpuError::InvalidLength { .. } => InvalidLength::new_err(err.to_string()),
            PpuError::UnknownLetter { .. } => UnknownLetter::new_err(err.to_string()),
            PpuError::EmptyLetter => EmptyLetter::new_err(err.to_string()),
            PpuError::UnknownDigraph { .. } => UnknownDigraph::new_err(err.to_string()),
            PpuError::EmptyDigraph => EmptyDigraph::new_err(err.to_string()),
        }
    }
}

impl From<VerifierError> for PyErr {
    fn from(err: VerifierError) -> PyErr {
        match err {
            VerifierError::EmptyVerifier => EmptyVerifier::new_err(err.to_string()),
            VerifierError::InvalidVerifier { .. } => InvalidVerifier::new_err(err.to_string()),
            VerifierError::UnexpectedComputation => UnexpectedComputation::new_err(err.to_string()),
        }
    }
}

impl From<GenerateError> for PyErr {
    fn from(err: GenerateError) -> PyErr {
        match err {
            GenerateError::InvalidRange { .. } => InvalidRange::new_err(err.to_string()),
            GenerateError::InvalidInput { .. } => InvalidInput::new_err(err.to_string()),
            GenerateError::InsufficientRange { .. } => InsufficientRange::new_err(err.to_string()),
            GenerateError::UnexpectedGeneration(_) => UnexpectedGeneration::new_err(err.to_string()),
        }
    }
}


#[pyclass(frozen)]
struct Ppu {
    #[pyo3(get)]
    raw: String,
    #[pyo3(get)]
    numeric: u32,
    #[pyo3(get)]
    normalized: String,
    #[pyo3(get)]
    verifier: char,
    format: enums::PpuFormat,
}

#[pymethods]
impl Ppu {
    /// Create a new `Ppu` instance.
    #[new]
    fn new(ppu: &str) -> PyResult<Self> {
        let raw = ppu;
        let normalized = utils::normalize_ppu(&raw)?;
        let format = utils::get_ppu_format(&raw).unwrap();
        let numeric = utils::ppu_to_numeric(&normalized)?;
        let verifier = utils::calculate_verifier(numeric)?;
        Ok(Self { raw: ppu.to_string(), numeric, normalized, verifier, format })
    }

    #[getter]
    fn format(&self) -> String {
        self.format.as_str().to_string()
    }

    #[getter]
    fn complete(&self) -> String {
        format!("{}-{}", self.normalized, self.verifier)
    }

    fn __repr__(&self) -> String {
        format!(
            "Ppu(\
                raw='{}', \
                normalized='{}', \
                numeric='{}', \
                verifier='{}', \
                complete='{}', \
                format='{}')",
            self.raw,
            self.normalized,
            self.numeric,
            self.verifier,
            self.complete(),
            self.format()
        )
    }
}


#[pyfunction]
fn normalize_ppu(ppu: &str) -> PyResult<String> {
    match utils::normalize_ppu(ppu) {
        Ok(normalized) => Ok(normalized),
        Err(msg) => Err(msg.into()),
    }
}


#[pyfunction]
fn ppu_to_numeric(ppu: &str) -> PyResult<u32> {
    match utils::ppu_to_numeric(ppu) {
        Ok(numeric) => Ok(numeric),
        Err(msg) => Err(msg.into()),
    }
}

#[pyfunction]
fn calculate_verifier(digits: u32) -> PyResult<String> {
    match utils::calculate_verifier(digits) {
        Ok(verifier) => Ok(verifier.to_string()),
        Err(msg) => Err(msg.into()),
    }
}


#[pyfunction]
fn validate_rut(digits: u32, verifier: &str) -> PyResult<bool> {
    match utils::validate_rut(digits, verifier) {
        Ok(result) => Ok(result),
        Err(msg) => Err(msg.into()),
    }
}


#[pyfunction]
#[pyo3(signature = (n, min, max, seed=None))]
fn generate(
        py: Python<'_>,
        n: i32,
        min: i32,
        max: i32,
        seed: Option<i64>
) -> PyResult<Py<PyAny>> {
    match utils::generate(n, min, max, seed) {
        Ok(ruts) => {
            let list = PyList::empty(py);
            for r in ruts {
                let dict = PyDict::new(py);
                dict.set_item("correlative", r.correlative)?;
                dict.set_item("verifier", r.verifier)?;
                list.append(dict)?;
            }
            Ok(list.into())
        }
        Err(msg) => Err(msg.into()),
    }
}


#[pymodule]
pub fn rs_verify(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_verifier, m)?)?;
    m.add_function(wrap_pyfunction!(ppu_to_numeric, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_ppu, m)?)?;
    m.add_function(wrap_pyfunction!(validate_rut, m)?)?;
    m.add_function(wrap_pyfunction!(generate, m)?)?;
    m.add_class::<Ppu>()?;

    m.add("PpuException", m.py().get_type::<PpuException>())?;
    m.add("UnknownFormat", m.py().get_type::<UnknownFormat>())?;
    m.add("InvalidLength", m.py().get_type::<InvalidLength>())?;
    m.add("UnknownLetter", m.py().get_type::<UnknownLetter>())?;
    m.add("EmptyLetter", m.py().get_type::<EmptyLetter>())?;
    m.add("UnknownDigraph", m.py().get_type::<UnknownDigraph>())?;
    m.add("EmptyDigraph", m.py().get_type::<EmptyDigraph>())?;

    m.add("VerifierException", m.py().get_type::<VerifierException>())?;
    m.add("EmptyVerifier", m.py().get_type::<EmptyVerifier>())?;
    m.add("InvalidVerifier", m.py().get_type::<InvalidVerifier>())?;
    m.add("UnexpectedComputation", m.py().get_type::<UnexpectedComputation>())?;

    m.add("GenerateException", m.py().get_type::<GenerateException>())?;
    m.add("InvalidRange", m.py().get_type::<InvalidRange>())?;
    m.add("InvalidInput", m.py().get_type::<InvalidInput>())?;
    m.add("InsufficientRange", m.py().get_type::<InsufficientRange>())?;
    m.add("UnexpectedGeneration", m.py().get_type::<UnexpectedGeneration>())?;

    Ok(())
}