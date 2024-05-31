use pyo3::prelude::*;
use pyo3_chrono::NaiveDate as PyNaiveDate;

#[pyclass]
#[derive(Debug, Copy, Clone)]
pub struct Review {
    #[pyo3(get)]
    pub date: PyNaiveDate,
    #[pyo3(get)]
    pub cycle: PyNaiveDate,
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
        date: PyNaiveDate,
        cycle: PyNaiveDate,
        content_type_id: u32,
        from_member_id: u32,
        to_member_id: u32,
        id: u32,
        skill: f64,
        teamwork: f64,
        aggregate: f64,
    ) -> Self {
        Self {
            date,
            cycle,
            content_type_id,
            from_member_id,
            to_member_id,
            id,
            skill,
            teamwork,
            aggregate,
        }
    }
}
