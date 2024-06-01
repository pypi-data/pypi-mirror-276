#[derive(Debug, Default, Clone)]
pub struct MinMax {
    pub min_value: f64,
    pub max_value: f64,
}

impl MinMax {
    pub fn new(min_value: f64, max_value: f64) -> Self {
        Self {
            min_value,
            max_value,
        }
    }

    pub fn update(&mut self, value: f64) {
        if value < self.min_value {
            self.min_value = value;
        }
        if value > self.max_value {
            self.max_value = value;
        }
    }

    pub fn range(&self) -> f64 {
        self.max_value - self.min_value
    }
}
