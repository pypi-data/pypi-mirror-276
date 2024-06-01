use pyo3::types::{PyDate, PyDateAccess};
use pyo3::{Bound, PyResult, Python};

#[derive(Debug, Clone, Copy, Eq, PartialEq)]
pub struct DateWrap {
    year: i32,
    month: u8,
    day: u8,
}

impl DateWrap {
    pub const MIN: DateWrap = Self {
        year: 1970,
        month: 1,
        day: 1,
    };

    pub fn from_python(py_date: &Bound<'_, PyDate>) -> DateWrap {
        DateWrap {
            year: py_date.get_year(),
            month: py_date.get_month(),
            day: py_date.get_day(),
        }
    }

    pub fn to_python(self, py: Python) -> PyResult<Bound<'_, PyDate>> {
        PyDate::new_bound(py, self.year, self.month, self.day)
    }
}
