use pyo3::prelude::*;
use pyo3_chrono::NaiveDate as PyNaiveDate;

use crate::delta::PeerRankScoreDeltaData;

#[pyclass]
#[derive(Debug, Clone)]
pub struct PeerRankScoreData {
    #[pyo3(get)]
    pub to_member_id: u32,
    #[pyo3(get)]
    pub date: PyNaiveDate,
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
            date: PyNaiveDate::from(chrono::NaiveDate::MIN),

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
        date: PyNaiveDate,
        skill: f64,
        teamwork: f64,
        aggregate: f64,
    ) -> Self {
        Self {
            to_member_id,
            date,
            skill,
            teamwork,
            aggregate,
            deltas: Vec::new(),
        }
    }
}
