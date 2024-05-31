use pyo3::exceptions;
use pyo3_chrono::NaiveDate as PyNaiveDate;
use std::collections::HashMap;

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};

use crate::boundaries::PeerRankScoreBoundaries;
use crate::peerrank::PeerRankCalculator;
use crate::prs::PeerRankScoreData;
use crate::review::Review;
use crate::row::ExplodedRow;
use crate::trend::_get_trend_type_values;

pub mod boundaries;
pub mod delta;
pub mod minmax;
pub mod peerrank;
pub mod prs;
pub mod review;
pub mod row;
pub mod trend;

#[pyclass]
struct PeerRank {
    calculator: PeerRankCalculator,
}

fn get_float(kwargs: &PyDict, key: &str) -> f64 {
    kwargs
        .get_item(key)
        .and_then(|o| o.extract::<f64>().ok())
        .unwrap_or(0.)
}

#[pymethods]
impl PeerRank {
    #[new]
    #[args(kwargs = "**")]
    #[allow(clippy::too_many_arguments)]
    fn new(kwargs: Option<&PyDict>) -> PyResult<PeerRank> {
        if let Some(kwargs) = kwargs {
            let min_skill: f64 = get_float(kwargs, "min_skill");
            let max_skill: f64 = get_float(kwargs, "max_skill");
            let min_teamwork: f64 = get_float(kwargs, "min_teamwork");
            let max_teamwork: f64 = get_float(kwargs, "max_teamwork");
            let min_aggregate: f64 = get_float(kwargs, "min_aggregate");
            let max_aggregate: f64 = get_float(kwargs, "max_aggregate");
            let prs_by_employee_id: &PyDict = kwargs
                .get_item("prs_by_employee_id")
                .and_then(|o| o.downcast::<PyDict>().ok())
                .unwrap();
            Ok(PeerRank {
                calculator: create_calculator(
                    prs_by_employee_id,
                    min_skill,
                    max_skill,
                    min_teamwork,
                    max_teamwork,
                    min_aggregate,
                    max_aggregate,
                ),
            })
        } else {
            Err(PyErr::new::<exceptions::PyTypeError, _>(
                "Invalid arguments",
            ))
        }
    }

    fn process_date(
        &mut self,
        reviews_list: &PyList,
        date: PyNaiveDate,
    ) -> PyResult<(Vec<PeerRankScoreData>, Vec<ExplodedRow>)> {
        let reviews: Vec<Review> = reviews_list.iter().map(|i| i.extract().unwrap()).collect();
        let exploded_rows_for_date = self.calculator.explode_date(&reviews, date);
        let prs = self.calculator.process_date(&exploded_rows_for_date);
        Ok((prs, exploded_rows_for_date))
    }

    fn get_prs(&mut self, employee_id: u32) -> PyResult<PeerRankScoreData> {
        Ok(self.calculator.get_prs(employee_id).clone())
    }
}

fn create_calculator(
    prs_by_employee_id: &PyDict,
    min_skill: f64,
    max_skill: f64,
    min_teamwork: f64,
    max_teamwork: f64,
    min_aggregate: f64,
    max_aggregate: f64,
) -> PeerRankCalculator {
    let mut _prs_by_employee_id = HashMap::new();
    for (k, v) in prs_by_employee_id.iter() {
        let employee_id = FromPyObject::extract(k).unwrap();
        let prs = v.extract().unwrap();
        _prs_by_employee_id.insert(employee_id, prs);
    }
    PeerRankCalculator {
        prs_by_employee_id: _prs_by_employee_id,
        prs_boundaries: PeerRankScoreBoundaries::new(
            min_skill,
            max_skill,
            min_teamwork,
            max_teamwork,
            min_aggregate,
            max_aggregate,
        ),
    }
}

#[pyfunction]
fn get_trend_type_values(prs_values: &PyList, threshold: f64) -> Vec<i32> {
    let vec: Vec<f64> = prs_values.iter().map(|i| i.extract().unwrap()).collect();
    _get_trend_type_values(&vec, threshold)
}

/// This module implements the Peer Rank algorithm in Rust
#[pymodule]
fn prscalc(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PeerRank>()?;
    m.add_class::<PeerRankScoreData>()?;
    m.add_class::<Review>()?;
    m.add_class::<ExplodedRow>()?;
    m.add_function(wrap_pyfunction!(get_trend_type_values, m)?)?;
    Ok(())
}
