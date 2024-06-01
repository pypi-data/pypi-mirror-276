use std::collections::HashMap;

use pyo3::prelude::*;
use pyo3::types::{PyDate, PyDict, PyList};
use pyo3::wrap_pyfunction;

use crate::boundaries::PeerRankScoreBoundaries;
use crate::peerrank::PeerRankCalculator;
use crate::prs::PeerRankScoreData;
use crate::py_bind::DateWrap;
use crate::review::Review;
use crate::row::ExplodedRow;
use crate::trend::_get_trend_type_values;

pub mod boundaries;
pub mod delta;
pub mod minmax;
pub mod peerrank;
pub mod prs;
mod py_bind;
pub mod review;
pub mod row;
pub mod trend;

#[pyclass]
struct PeerRank {
    calculator: PeerRankCalculator,
}

fn get_float(o_kwargs: Option<&Bound<'_, PyDict>>, key: &str) -> PyResult<f64> {
    o_kwargs
        .and_then(|kwargs| kwargs.get_item(key).ok().flatten())
        .map::<Result<f64, _>, _>(|v| v.extract::<f64>())
        .unwrap_or(Ok(0.))
}

#[pymethods]
impl PeerRank {
    #[new]
    #[pyo3(signature = (prs_by_employee_id, **kwargs))]
    fn py_new(
        prs_by_employee_id: &Bound<'_, PyDict>,
        kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<PeerRank> {
        let min_skill: f64 = get_float(kwargs, "min_skill")?;
        let max_skill: f64 = get_float(kwargs, "max_skill")?;
        let min_teamwork: f64 = get_float(kwargs, "min_teamwork")?;
        let max_teamwork: f64 = get_float(kwargs, "max_teamwork")?;
        let min_aggregate: f64 = get_float(kwargs, "min_aggregate")?;
        let max_aggregate: f64 = get_float(kwargs, "max_aggregate")?;

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
    }

    fn process_date(
        &mut self,
        reviews_list: &Bound<'_, PyList>,
        date: &Bound<'_, PyDate>,
    ) -> PyResult<(Vec<PeerRankScoreData>, Vec<ExplodedRow>)> {
        let reviews: Vec<Review> = reviews_list.iter().map(|i| i.extract().unwrap()).collect();
        let exploded_rows_for_date = self
            .calculator
            .explode_date(&reviews, &DateWrap::from_python(date));
        let prs = self.calculator.process_date(&exploded_rows_for_date);
        Ok((prs, exploded_rows_for_date))
    }

    fn get_prs(&mut self, employee_id: u32) -> PyResult<PeerRankScoreData> {
        Ok(self.calculator.get_prs(employee_id).clone())
    }
}

fn create_calculator(
    prs_by_employee_id: &Bound<'_, PyDict>,
    min_skill: f64,
    max_skill: f64,
    min_teamwork: f64,
    max_teamwork: f64,
    min_aggregate: f64,
    max_aggregate: f64,
) -> PeerRankCalculator {
    let mut _prs_by_employee_id = HashMap::new();
    for (k, v) in prs_by_employee_id.iter() {
        let employee_id = FromPyObject::extract_bound(&k).unwrap();
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
fn get_trend_type_values(prs_values: &Bound<'_, PyList>, threshold: f64) -> Vec<i32> {
    let vec: Vec<f64> = prs_values.iter().map(|i| i.extract().unwrap()).collect();
    _get_trend_type_values(&vec, threshold)
}

/// This module implements the Peer Rank algorithm in Rust
#[pymodule]
fn prscalc(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PeerRank>()?;
    m.add_class::<PeerRankScoreData>()?;
    m.add_class::<Review>()?;
    m.add_class::<ExplodedRow>()?;
    m.add_function(wrap_pyfunction!(get_trend_type_values, m)?)?;
    Ok(())
}
