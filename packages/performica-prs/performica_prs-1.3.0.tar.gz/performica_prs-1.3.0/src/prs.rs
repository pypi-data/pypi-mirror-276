use pyo3::prelude::*;
use pyo3::types::PyDate;

use crate::delta::PeerRankScoreDeltaData;
use crate::py_bind::DateWrap;

#[pyclass]
#[derive(Debug, Clone)]
pub struct PeerRankScoreData {
    #[pyo3(get)]
    pub to_member_id: u32,
    pub _date: DateWrap,
    #[pyo3(get)]
    pub skill: f64,
    #[pyo3(get)]
    pub teamwork: f64,
    #[pyo3(get)]
    pub aggregate: f64,
    #[pyo3(get)]
    pub deltas: Vec<PeerRankScoreDeltaData>,
}

impl PeerRankScoreData {
    pub fn zero(employee_id: u32) -> Self {
        Self {
            to_member_id: employee_id,
            _date: DateWrap::MIN,
            skill: 0.0,
            teamwork: 0.0,
            aggregate: 0.0,
            deltas: Vec::default(),
        }
    }
}

#[pymethods]
impl PeerRankScoreData {
    #[new]
    fn new(
        to_member_id: u32,
        date: &Bound<'_, PyDate>,
        skill: f64,
        teamwork: f64,
        aggregate: f64,
    ) -> Self {
        let _date = DateWrap::from_python(date);
        Self {
            to_member_id,
            _date,
            skill,
            teamwork,
            aggregate,
            deltas: Vec::new(),
        }
    }

    #[getter]
    fn date<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDate>> {
        self._date.to_python(py)
    }
}
