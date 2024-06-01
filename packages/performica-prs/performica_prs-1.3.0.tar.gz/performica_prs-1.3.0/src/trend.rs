/// Exponentially Weighted Moving Average
fn ewma(arr: &[f64], window: i32) -> Vec<f64> {
    let n = arr.len();
    let mut result: Vec<f64> = Vec::new();
    let alpha_rev = 1. - 2. / (window as f64 + 1.);
    let mut w = 1.;
    let mut prev_value = arr[0];
    result.push(prev_value);
    for (i, item) in arr.iter().enumerate().take(n).skip(1) {
        w += alpha_rev.powi(i as i32);
        prev_value = prev_value * alpha_rev + item;
        result.push(prev_value / w);
    }
    result
}

/// Weighted Moving Average Convergence/Divergence
fn wmacd(arr: &[f64]) -> Vec<f64> {
    let ewma12 = ewma(arr, 12);
    let ewma26 = ewma(arr, 26);
    let mut difference: Vec<f64> = Vec::new();
    for i in 0..arr.len() {
        difference.push(ewma12[i] - ewma26[i])
    }
    ewma(&difference, 9)
}

pub fn _get_trend_type_values(arr: &[f64], threshold: f64) -> Vec<i32> {
    const TREND_TYPE_UP: i32 = 1;
    const TREND_TYPE_STABLE: i32 = 0;
    const TREND_TYPE_DOWN: i32 = -1;
    let wmacd_values = wmacd(arr);
    let mut result: Vec<i32> = Vec::new();
    for value in wmacd_values {
        if value > threshold {
            result.push(TREND_TYPE_UP);
        } else if value < -threshold {
            result.push(TREND_TYPE_DOWN)
        } else {
            result.push(TREND_TYPE_STABLE)
        }
    }
    result
}
