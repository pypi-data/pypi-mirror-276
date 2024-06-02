use pyo3::{exceptions::PyValueError, prelude::*};
use edit_distance::edit_distance;
use indicatif::{ProgressBar, ProgressStyle};


/// Calculates the levenshtein distance between two lists of strings.
#[pyfunction]
fn find_best_match_levenshtein(companies: Vec<(String, u64)>, patent_applicant: Vec<(String, f32)>, threshold: f32) -> PyResult<(Vec<u64>, Vec<f32>)> {
    if threshold < 0.0 || threshold > 1.0 {
        return Err(PyValueError::new_err("threshold must be between 0 and 1"));
    }
    // Progress bar.
    let progress_bar = ProgressBar::new((patent_applicant.len()) as u64);
    progress_bar.set_style(
        ProgressStyle::default_bar()
            .template("[{elapsed_precise}] {bar:70.cyan/blue} {percent}% - Calculating levenshtein distance for dataset")
            .unwrap()
            .progress_chars("=> "),
    );
    progress_bar.set_position(0);
    
    let mut valid_matches: (Vec<u64>, Vec<f32>) = (vec![], vec![]);
    for (idx, (pa_name, score)) in patent_applicant.iter().enumerate() {
        let formatted_pa = pa_name.to_lowercase();
        let mut best_match: (usize, String, u64, f32) = (100, "".to_string(), 0, 0.0);
        for (company_name, org_nr ) in companies.iter() {
            let formatted_company = company_name.to_lowercase();
            let levenshtein_distance: usize = edit_distance(formatted_pa.trim(), formatted_company.trim());
            if levenshtein_distance == 0 {
                valid_matches.0.push(*org_nr);
                valid_matches.1.push(*score);
                break
            }
            if levenshtein_distance <= best_match.0 {
                best_match = (levenshtein_distance, formatted_company.trim().to_string(), *org_nr, *score);
            }
        }
        if (best_match.0 as f32 / best_match.1.len() as f32) <= 1.0-threshold {
            valid_matches.0.push(best_match.2);
            valid_matches.1.push(best_match.3);
        }
        progress_bar.set_position((idx+1) as u64);
    }
    Ok(valid_matches)
}

/// A Python module implemented in Rust.
#[pymodule]
fn nipo_company_distance(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_best_match_levenshtein, m)?)?;
    Ok(())
}
