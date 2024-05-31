use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3_chrono::NaiveDate as PyNaiveDate;

#[pyclass]
#[derive(Debug, Clone)]
pub struct ExplodedRow {
    #[pyo3(get)]
    pub content_type_id: u32,
    #[pyo3(get)]
    pub from_member_id: u32,
    #[pyo3(get)]
    pub date: PyNaiveDate,
    #[pyo3(get)]
    pub cycle: PyNaiveDate,
    #[pyo3(get)]
    pub id_1: u32,
    #[pyo3(get)]
    pub id_2: u32,
    #[pyo3(get)]
    pub to_member_id_1: u32,
    #[pyo3(get)]
    pub to_member_id_2: u32,
    #[pyo3(get)]
    pub skill_reviewer_weight: f64,
    #[pyo3(get)]
    pub skill_spread_weight: f64,
    #[pyo3(get)]
    pub skill_expectation_weight: f64,
    #[pyo3(get)]
    pub skill_increment: f64,
    #[pyo3(get)]
    pub teamwork_reviewer_weight: f64,
    #[pyo3(get)]
    pub teamwork_spread_weight: f64,
    #[pyo3(get)]
    pub teamwork_expectation_weight: f64,
    #[pyo3(get)]
    pub teamwork_increment: f64,
    #[pyo3(get)]
    pub aggregate_reviewer_weight: f64,
    #[pyo3(get)]
    pub aggregate_spread_weight: f64,
    #[pyo3(get)]
    pub aggregate_expectation_weight: f64,
    #[pyo3(get)]
    pub aggregate_increment: f64,
}

#[pymethods]
impl ExplodedRow {
    pub fn to_list<'p>(&self, py: Python<'p>) -> PyResult<&'p PyList> {
        let result = PyList::new(py, vec![self.content_type_id, self.from_member_id]);
        result.append(self.date)?;
        result.append(self.cycle)?;
        result.append(self.id_1)?;
        result.append(self.id_2)?;
        result.append(self.to_member_id_1)?;
        result.append(self.to_member_id_2)?;
        result.append(self.skill_reviewer_weight)?;
        result.append(self.skill_spread_weight)?;
        result.append(self.skill_expectation_weight)?;
        result.append(self.skill_increment)?;
        result.append(self.teamwork_reviewer_weight)?;
        result.append(self.teamwork_spread_weight)?;
        result.append(self.teamwork_expectation_weight)?;
        result.append(self.teamwork_increment)?;
        result.append(self.aggregate_reviewer_weight)?;
        result.append(self.aggregate_spread_weight)?;
        result.append(self.aggregate_expectation_weight)?;
        result.append(self.aggregate_increment)?;
        Ok(result)
    }
}
