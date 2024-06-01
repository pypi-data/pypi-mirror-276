use crate::py_bind::DateWrap;
use pyo3::prelude::*;
use pyo3::types::PyDate;

#[pyclass]
#[derive(Debug, Clone)]
pub struct PeerRankScoreDeltaData {
    pub _date: DateWrap,
    #[pyo3(get)]
    pub survey_request_id: u32,
    #[pyo3(get)]
    pub to_member_id: u32,
    #[pyo3(get)]
    pub teamwork: f64,
    #[pyo3(get)]
    pub skill: f64,
    #[pyo3(get)]
    pub aggregate: f64,
}

#[pymethods]
impl PeerRankScoreDeltaData {
    pub fn massage(&mut self) {
        self.skill = self.skill.cbrt();
        self.teamwork = self.teamwork.cbrt();
        self.aggregate = self.aggregate.cbrt();
    }

    #[getter]
    fn date<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDate>> {
        self._date.to_python(py)
    }
}
