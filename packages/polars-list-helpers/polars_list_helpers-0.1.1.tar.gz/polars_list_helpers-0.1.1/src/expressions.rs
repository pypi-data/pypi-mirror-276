#![allow(clippy::unused_unit)]
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::cmp::Ordering;

#[polars_expr(output_type=Float64)]
fn closest_elem(inputs: &[Series]) -> PolarsResult<Series> {
    let lists_to_check = inputs[0].list()?;
    let target = inputs[1].f64()?;

    let out: Float64Chunked = lists_to_check
        .into_iter()
        .zip(target.into_iter())
        .map(|(list_opt, target_opt)| {
            let ca = list_opt.unwrap();
            let ca = ca.f64().unwrap();
            let v = target_opt.unwrap();
            ca
                    .into_no_null_iter()
                    .map(|x_val| (x_val - v).abs())
                    .enumerate()
                    .min_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap_or(Ordering::Equal))
                    .and_then(|(min_idx, _)| ca.get(min_idx))
            
        })
        .collect();

    Ok(out.into_series())
}


#[polars_expr(output_type=UInt32)]
fn closest_elem_index(inputs: &[Series]) -> PolarsResult<Series> {
    let lists_to_check = inputs[0].list()?;
    let target = inputs[1].f64()?;

    let out: UInt32Chunked = lists_to_check
        .into_iter()
        .zip(target.into_iter())
        .map(|(list_opt, target_opt)| {
            let ca = list_opt.unwrap();
            let ca = ca.f64().unwrap();
            let v = target_opt.unwrap();
            ca.into_no_null_iter()
                .map(|x_val| (x_val - v).abs())
                .enumerate()
                .min_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap_or(Ordering::Equal))
                .map(|(min_idx, _)| min_idx as u32)
        })
        .collect();

    Ok(out.into_series())
}
