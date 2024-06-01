use crate::py_bind::DateWrap;
use pyo3::prelude::*;
use pyo3::types::PyDate;

#[pyclass]
#[derive(Debug, Copy, Clone)]
pub struct Review {
    _date: DateWrap,
    pub _cycle: DateWrap,
    #[pyo3(get)]
    pub content_type_id: u32,
    #[pyo3(get)]
    pub from_member_id: u32,
    #[pyo3(get)]
    pub to_member_id: u32,
    #[pyo3(get)]
    pub id: u32,
    #[pyo3(get)]
    pub skill: f64,
    #[pyo3(get)]
    pub teamwork: f64,
    #[pyo3(get)]
    pub aggregate: f64,
}

#[pymethods]
impl Review {
    #[new]
    #[allow(clippy::too_many_arguments)]
    fn new(
        date: &Bound<'_, PyDate>,
        cycle: &Bound<'_, PyDate>,
        content_type_id: u32,
        from_member_id: u32,
        to_member_id: u32,
        id: u32,
        skill: f64,
        teamwork: f64,
        aggregate: f64,
    ) -> Self {
        let _date = DateWrap::from_python(date);
        let _cycle = DateWrap::from_python(cycle);
        Self {
            _date,
            _cycle,
            content_type_id,
            from_member_id,
            to_member_id,
            id,
            skill,
            teamwork,
            aggregate,
        }
    }

    #[getter]
    fn date<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDate>> {
        self._date.to_python(py)
    }

    #[getter]
    fn cycle<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDate>> {
        self._cycle.to_python(py)
    }
}
