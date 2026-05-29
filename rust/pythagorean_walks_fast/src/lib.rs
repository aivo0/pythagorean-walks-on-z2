use pyo3::exceptions::{PyAssertionError, PyOverflowError, PyValueError};
use pyo3::prelude::*;
use std::collections::{BTreeSet, HashMap, HashSet};
use std::sync::{Mutex, OnceLock};

#[derive(Clone, Copy)]
struct LatticePair {
    first: (i64, i64),
    second: (i64, i64),
    determinant: i64,
}

static LATTICE_PAIRS_25_1435: OnceLock<Vec<LatticePair>> = OnceLock::new();
static LATTICE_PAIR_REGISTRY: OnceLock<Mutex<HashMap<String, Vec<LatticePair>>>> = OnceLock::new();

fn is_square_i128(n: i128) -> bool {
    if n < 0 {
        return false;
    }
    let mut lo = 0_i128;
    let mut hi = 1_i128;
    while hi.saturating_mul(hi) < n {
        hi = hi.saturating_mul(2);
    }
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        let square = mid * mid;
        if square == n {
            return true;
        }
        if square < n {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    false
}

fn edge_delta_i128(dx: i128, dy: i128) -> bool {
    if dx == 0 || dy == 0 {
        return false;
    }
    is_square_i128(dx * dx + dy * dy)
}

fn certificate_valid_i128(target: (i128, i128), midpoint: (i128, i128)) -> bool {
    edge_delta_i128(midpoint.0, midpoint.1)
        && edge_delta_i128(target.0 - midpoint.0, target.1 - midpoint.1)
}

fn factorize(n: u64) -> Vec<(u64, u32)> {
    let mut remaining = n;
    let mut factors = Vec::new();
    let mut exponent = 0_u32;
    while remaining % 2 == 0 {
        remaining /= 2;
        exponent += 1;
    }
    if exponent > 0 {
        factors.push((2, exponent));
    }

    let mut candidate = 3_u64;
    while candidate <= remaining / candidate {
        exponent = 0;
        while remaining % candidate == 0 {
            remaining /= candidate;
            exponent += 1;
        }
        if exponent > 0 {
            factors.push((candidate, exponent));
        }
        candidate += 2;
    }
    if remaining > 1 {
        factors.push((remaining, 1));
    }
    factors
}

fn positive_divisors_vec(n: u64) -> Vec<u64> {
    let mut divisors = vec![1_u64];
    for (prime, exponent) in factorize(n) {
        let current = divisors.clone();
        let mut power = 1_u64;
        for _ in 0..=exponent {
            for divisor in &current {
                divisors.push(divisor * power);
            }
            power *= prime;
        }
        divisors = divisors[current.len()..].to_vec();
    }
    divisors.sort_unstable();
    divisors
}

fn divisor_residue_classes_vec(n: u64, modulus: u64) -> Vec<u64> {
    let mut residues = BTreeSet::from([1 % modulus]);
    for (prime, exponent) in factorize(n) {
        let mut prime_powers = Vec::with_capacity((exponent + 1) as usize);
        let mut power = 1_u64 % modulus;
        for _ in 0..=exponent {
            prime_powers.push(power);
            power = (power * (prime % modulus)) % modulus;
        }

        let mut next = BTreeSet::new();
        for residue in &residues {
            for prime_power in &prime_powers {
                next.insert((residue * prime_power) % modulus);
            }
        }
        residues = next;
    }
    residues.into_iter().collect()
}

fn isqrt_i128(n: i128) -> i128 {
    let mut lo = 0_i128;
    let mut hi = 1_i128;
    while hi.saturating_mul(hi) < n {
        hi = hi.saturating_mul(2);
    }
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        let square = mid * mid;
        if square == n {
            return mid;
        }
        if square < n {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    hi
}

fn determinant(first: (i64, i64), second: (i64, i64)) -> i128 {
    first.0 as i128 * second.1 as i128 - first.1 as i128 * second.0 as i128
}

fn determinant_i128(first: (i128, i128), second: (i128, i128)) -> i128 {
    first.0 * second.1 - first.1 * second.0
}

fn gcd_i128(mut a: i128, mut b: i128) -> i128 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn gcd_i64(a: i64, b: i64) -> i64 {
    gcd_i128(a as i128, b as i128) as i64
}

fn extended_gcd_i128(first: i128, second: i128) -> (i128, i128, i128) {
    let mut old_r = first;
    let mut r = second;
    let mut old_s = 1_i128;
    let mut s = 0_i128;
    let mut old_t = 0_i128;
    let mut t = 1_i128;
    while r != 0 {
        let quotient = old_r.div_euclid(r);
        let next_r = old_r - quotient * r;
        old_r = r;
        r = next_r;

        let next_s = old_s - quotient * s;
        old_s = s;
        s = next_s;

        let next_t = old_t - quotient * t;
        old_t = t;
        t = next_t;
    }
    if old_r < 0 {
        (-old_r, -old_s, -old_t)
    } else {
        (old_r, old_s, old_t)
    }
}

fn modular_inverse_i128(value: i128, modulus: i128) -> Option<i128> {
    let (gcd, coefficient, _other) = extended_gcd_i128(value.rem_euclid(modulus), modulus);
    if gcd == 1 {
        Some(coefficient.rem_euclid(modulus))
    } else {
        None
    }
}

fn add_mod_u128(first: u128, second: u128, modulus: u128) -> u128 {
    if first >= modulus - second {
        first - (modulus - second)
    } else {
        first + second
    }
}

fn mul_mod_i128(first: i128, second: i128, modulus: i128) -> i128 {
    let modulus_u = modulus as u128;
    let mut result = 0_u128;
    let mut base = first.rem_euclid(modulus) as u128;
    let mut multiplier = second.rem_euclid(modulus) as u128;
    while multiplier > 0 {
        if multiplier & 1 == 1 {
            result = add_mod_u128(result, base, modulus_u);
        }
        multiplier >>= 1;
        if multiplier > 0 {
            base = add_mod_u128(base, base, modulus_u);
        }
    }
    result as i128
}

fn checked_parallel_factor_add(left: i128, right: i128) -> PyResult<i128> {
    left.checked_add(right)
        .ok_or_else(|| PyOverflowError::new_err("parallel factor formula exceeded i128"))
}

fn checked_parallel_factor_sub(left: i128, right: i128) -> PyResult<i128> {
    left.checked_sub(right)
        .ok_or_else(|| PyOverflowError::new_err("parallel factor formula exceeded i128"))
}

fn checked_parallel_factor_mul(left: i128, right: i128) -> PyResult<i128> {
    left.checked_mul(right)
        .ok_or_else(|| PyOverflowError::new_err("parallel factor formula exceeded i128"))
}

fn factor_congruence_holds(target: (i64, i64), direction: (i64, i64), factor: i64) -> bool {
    let u = direction.0 as i128;
    let v = direction.1 as i128;
    let c = isqrt_i128(u * u + v * v);
    let determinant_leg = determinant(direction, target);
    if determinant_leg == 0 {
        return false;
    }
    let dot_product = target.0 as i128 * u + target.1 as i128 * v;
    let determinant_square = determinant_leg * determinant_leg;
    let factor = factor as i128;
    let factor_square = factor * factor;
    (determinant_square + factor_square) % (2 * c * factor) == 0
        && (determinant_square - factor_square + 2 * factor * dot_product) % (2 * factor * c * c)
            == 0
}

fn parallel_direction_factor_congruence_data_i128(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Option<(i128, i128, i128)>> {
    let g = target.0 as i128;
    let h = target.1 as i128;
    let u = direction.0 as i128;
    let v = direction.1 as i128;
    let c = isqrt_i128(checked_parallel_factor_add(
        checked_parallel_factor_mul(u, u)?,
        checked_parallel_factor_mul(v, v)?,
    )?);
    let determinant_leg = checked_parallel_factor_sub(
        checked_parallel_factor_mul(u, h)?,
        checked_parallel_factor_mul(v, g)?,
    )?;
    if determinant_leg == 0 {
        return Ok(None);
    }

    let dot_product = checked_parallel_factor_add(
        checked_parallel_factor_mul(g, u)?,
        checked_parallel_factor_mul(h, v)?,
    )?;
    let determinant_square = checked_parallel_factor_mul(determinant_leg, determinant_leg)?;
    let factor = factor as i128;
    let factor_square = checked_parallel_factor_mul(factor, factor)?;

    let first_numerator = checked_parallel_factor_add(determinant_square, factor_square)?;
    let first_denominator =
        checked_parallel_factor_mul(checked_parallel_factor_mul(2, c)?, factor)?;
    if first_numerator % first_denominator != 0 {
        return Ok(None);
    }

    let second_numerator = checked_parallel_factor_add(
        checked_parallel_factor_sub(determinant_square, factor_square)?,
        checked_parallel_factor_mul(checked_parallel_factor_mul(2, factor)?, dot_product)?,
    )?;
    let second_denominator = checked_parallel_factor_mul(
        checked_parallel_factor_mul(checked_parallel_factor_mul(2, factor)?, c)?,
        c,
    )?;
    if second_numerator % second_denominator != 0 {
        return Ok(None);
    }

    Ok(Some((
        determinant_leg,
        first_numerator / first_denominator,
        second_numerator / second_denominator,
    )))
}

fn primitive_factor_determinant_residue_rows_i128(
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Vec<(i128, i128)>> {
    let u = direction.0 as i128;
    let v = direction.1 as i128;
    let c = isqrt_i128(u * u + v * v);
    let direction_norm = c * c;
    let factor_modulus = parallel_direction_factor_modulus(direction, factor)? as i128;
    let Some(inverse_u) = modular_inverse_i128(u, direction_norm) else {
        return Err(PyValueError::new_err(
            "direction x-coordinate must be invertible modulo its norm",
        ));
    };
    let factor = factor as i128;
    let factor_square = factor * factor;
    let target_dot_multiplier = mul_mod_i128(v, inverse_u, direction_norm);

    let mut rows = Vec::new();
    for determinant_residue in 0..factor_modulus {
        let determinant_square = determinant_residue * determinant_residue;
        if (determinant_square + factor_square) % (2 * c * factor) != 0 {
            continue;
        }

        let dot_numerator = factor_square - determinant_square;
        if dot_numerator % (2 * factor) != 0 {
            continue;
        }
        let factor_dot_residue = (dot_numerator / (2 * factor)).rem_euclid(direction_norm);
        let target_dot_residue =
            mul_mod_i128(target_dot_multiplier, determinant_residue, direction_norm);
        if factor_dot_residue != target_dot_residue {
            continue;
        }

        rows.push((determinant_residue, factor_dot_residue));
    }
    Ok(rows)
}

fn primitive_pythagorean_directions(max_parameter: i64) -> Vec<(i64, i64, i64)> {
    let mut directions = Vec::new();
    let mut seen = HashSet::new();
    for a in 2..=max_parameter {
        for b in 1..a {
            if (a - b) % 2 == 0 || gcd_i64(a, b) != 1 {
                continue;
            }
            let odd_leg = a * a - b * b;
            let even_leg = 2 * a * b;
            let hypotenuse = a * a + b * b;
            for (base_x, base_y) in [(odd_leg, even_leg), (even_leg, odd_leg)] {
                for x_sign in [-1, 1] {
                    for y_sign in [-1, 1] {
                        let row = (x_sign * base_x, y_sign * base_y, hypotenuse);
                        if seen.insert(row) {
                            directions.push(row);
                        }
                    }
                }
            }
        }
    }
    directions.sort_by_key(|row| (row.2, row.0.abs() + row.1.abs(), row.0, row.1));
    directions
}

fn generate_lattice_pairs(max_parameter: i64, max_determinant: Option<i64>) -> Vec<LatticePair> {
    let directions = primitive_pythagorean_directions(max_parameter);
    let mut pairs = Vec::new();
    for first in &directions {
        for second in &directions {
            let first_direction = (first.0, first.1);
            let second_direction = (second.0, second.1);
            let pair_determinant = determinant(first_direction, second_direction).abs() as i64;
            if pair_determinant == 0 {
                continue;
            }
            if max_determinant.is_some_and(|limit| pair_determinant > limit) {
                continue;
            }
            pairs.push(LatticePair {
                first: first_direction,
                second: second_direction,
                determinant: pair_determinant,
            });
        }
    }
    pairs
}

fn lattice_coefficients_i128(
    target: (i64, i64),
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> Option<(i128, i128)> {
    let determinant_value = determinant(first_direction, second_direction);
    if determinant_value == 0 {
        return None;
    }
    let first_numerator = target.0 as i128 * second_direction.1 as i128
        - target.1 as i128 * second_direction.0 as i128;
    let second_numerator =
        first_direction.0 as i128 * target.1 as i128 - first_direction.1 as i128 * target.0 as i128;
    if first_numerator % determinant_value != 0 || second_numerator % determinant_value != 0 {
        return None;
    }
    Some((
        first_numerator / determinant_value,
        second_numerator / determinant_value,
    ))
}

fn i128_to_i64(value: i128) -> Option<i64> {
    if value < i64::MIN as i128 || value > i64::MAX as i128 {
        None
    } else {
        Some(value as i64)
    }
}

fn lattice_coefficients_inner(
    target: (i64, i64),
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> Option<(i64, i64)> {
    let (first_coefficient, second_coefficient) =
        lattice_coefficients_i128(target, first_direction, second_direction)?;
    Some((
        i128_to_i64(first_coefficient)?,
        i128_to_i64(second_coefficient)?,
    ))
}

fn lattice_pair_witness_from_pairs(
    target: (i64, i64),
    pairs: &[LatticePair],
) -> Option<((i64, i64), (i64, i64), i64, i64, i64)> {
    for pair in pairs {
        let Some((first_coefficient, second_coefficient)) =
            lattice_coefficients_inner(target, pair.first, pair.second)
        else {
            continue;
        };
        if first_coefficient == 0 || second_coefficient == 0 {
            continue;
        }
        return Some((
            pair.first,
            pair.second,
            pair.determinant,
            first_coefficient,
            second_coefficient,
        ));
    }
    None
}

fn checked_i128_mul(left: i128, right: i128) -> PyResult<i128> {
    left.checked_mul(right)
        .ok_or_else(|| PyOverflowError::new_err("lattice midpoint exceeded i128"))
}

fn checked_axis_add(left: i128, right: i128) -> PyResult<i128> {
    left.checked_add(right)
        .ok_or_else(|| PyOverflowError::new_err("axis formula exceeded i128"))
}

fn checked_axis_sub(left: i128, right: i128) -> PyResult<i128> {
    left.checked_sub(right)
        .ok_or_else(|| PyOverflowError::new_err("axis formula exceeded i128"))
}

fn checked_axis_mul(left: i128, right: i128) -> PyResult<i128> {
    left.checked_mul(right)
        .ok_or_else(|| PyOverflowError::new_err("axis formula exceeded i128"))
}

fn checked_theorem3_mul(left: i128, right: i128) -> PyResult<i128> {
    left.checked_mul(right)
        .ok_or_else(|| PyOverflowError::new_err("theorem 3 formula exceeded i128"))
}

fn checked_theorem3_sub(left: i128, right: i128) -> PyResult<i128> {
    left.checked_sub(right)
        .ok_or_else(|| PyOverflowError::new_err("theorem 3 formula exceeded i128"))
}

fn checked_linear_delta_add(left: i128, right: i128) -> PyResult<i128> {
    left.checked_add(right)
        .ok_or_else(|| PyOverflowError::new_err("linear delta formula exceeded i128"))
}

fn checked_linear_delta_sub(left: i128, right: i128) -> PyResult<i128> {
    left.checked_sub(right)
        .ok_or_else(|| PyOverflowError::new_err("linear delta formula exceeded i128"))
}

fn checked_linear_delta_mul(left: i128, right: i128) -> PyResult<i128> {
    left.checked_mul(right)
        .ok_or_else(|| PyOverflowError::new_err("linear delta formula exceeded i128"))
}

fn pythagorean_triple_valid(triple: (i64, i64, i64)) -> bool {
    let a = triple.0 as i128;
    let b = triple.1 as i128;
    let c = triple.2 as i128;
    a > 0 && b > 0 && c > 0 && a * a + b * b == c * c
}

fn theorem3_midpoint_i128(
    target: (i64, i64),
    triple: (i64, i64, i64),
    x_sign: i64,
    y_sign: i64,
    divisor: i128,
    require_positive_coefficient: bool,
    invalid_certificate_is_assertion: bool,
) -> PyResult<Option<(i128, i128)>> {
    if ![-1, 1].contains(&x_sign) || ![-1, 1].contains(&y_sign) {
        return Err(PyValueError::new_err("x_sign and y_sign must be -1 or 1"));
    }
    if divisor == 0 {
        return Err(PyValueError::new_err("divisor must be nonzero"));
    }
    if !pythagorean_triple_valid(triple) {
        return Err(PyValueError::new_err(
            "triple must be a positive Pythagorean triple",
        ));
    }

    let g = target.0 as i128;
    let h = target.1 as i128;
    if g == 0 || h == 0 {
        return Ok(None);
    }
    let target_product = g * h;
    if target_product % divisor != 0 {
        return Ok(None);
    }

    let a = triple.0 as i128;
    let b = triple.1 as i128;
    let c = triple.2 as i128;
    let x_direction = x_sign as i128 * a;
    let y_direction = y_sign as i128 * b;
    if (c - x_direction) * g != (c + y_direction) * h - divisor {
        return Ok(None);
    }

    let coefficient = target_product / divisor;
    if require_positive_coefficient && coefficient <= 0 {
        return Ok(None);
    }

    let midpoint = (
        checked_theorem3_mul(x_direction, coefficient)?,
        checked_theorem3_mul(y_direction, coefficient)?,
    );
    let second_x = checked_theorem3_sub(g, midpoint.0)?;
    let second_y = checked_theorem3_sub(h, midpoint.1)?;
    if second_x != 0 && second_y != 0 {
        Ok(Some(midpoint))
    } else if invalid_certificate_is_assertion {
        Err(PyAssertionError::new_err(
            "theorem 3 relation did not produce a valid certificate",
        ))
    } else {
        Ok(None)
    }
}

fn linear_delta_direction_midpoint_i128(
    target: (i64, i64),
    direction: (i64, i64),
    delta_coefficients: (i64, i64),
) -> PyResult<Option<(i128, i128)>> {
    let u = direction.0 as i128;
    let v = direction.1 as i128;
    if !edge_delta_i128(u, v) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }

    let g = target.0 as i128;
    let h = target.1 as i128;
    let alpha = delta_coefficients.0 as i128;
    let beta = delta_coefficients.1 as i128;
    let direction_norm = checked_linear_delta_add(
        checked_linear_delta_mul(u, u)?,
        checked_linear_delta_mul(v, v)?,
    )?;
    let hypotenuse = isqrt_i128(direction_norm);
    let signed_delta = checked_linear_delta_add(
        checked_linear_delta_mul(alpha, g)?,
        checked_linear_delta_mul(beta, h)?,
    )?;
    let target_norm = checked_linear_delta_add(
        checked_linear_delta_mul(g, g)?,
        checked_linear_delta_mul(h, h)?,
    )?;
    let numerator = checked_linear_delta_sub(
        target_norm,
        checked_linear_delta_mul(signed_delta, signed_delta)?,
    )?;
    if numerator <= 0 || numerator % 2 != 0 {
        return Ok(None);
    }

    let dot_product = checked_linear_delta_add(
        checked_linear_delta_mul(g, u)?,
        checked_linear_delta_mul(h, v)?,
    )?;
    let denominator = checked_linear_delta_sub(
        dot_product,
        checked_linear_delta_mul(signed_delta, hypotenuse)?,
    )?;
    if denominator == 0 {
        return Ok(None);
    }
    let double_denominator = checked_linear_delta_mul(2, denominator)?;
    if numerator % double_denominator != 0 {
        return Ok(None);
    }

    let coefficient = numerator / double_denominator;
    if coefficient <= 0 {
        return Ok(None);
    }

    let midpoint = (
        checked_linear_delta_mul(coefficient, u)?,
        checked_linear_delta_mul(coefficient, v)?,
    );
    let second_x = checked_linear_delta_sub(g, midpoint.0)?;
    let second_y = checked_linear_delta_sub(h, midpoint.1)?;
    if second_x != 0 && second_y != 0 {
        Ok(Some(midpoint))
    } else {
        Ok(None)
    }
}

fn lattice_certificate_midpoint_i128(
    target: (i64, i64),
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> PyResult<Option<(i128, i128)>> {
    let Some((first_coefficient, second_coefficient)) =
        lattice_coefficients_i128(target, first_direction, second_direction)
    else {
        return Ok(None);
    };
    if first_coefficient == 0 || second_coefficient == 0 {
        return Ok(None);
    }
    Ok(Some((
        checked_i128_mul(first_coefficient, first_direction.0 as i128)?,
        checked_i128_mul(first_coefficient, first_direction.1 as i128)?,
    )))
}

fn registered_lattice_pairs() -> &'static Mutex<HashMap<String, Vec<LatticePair>>> {
    LATTICE_PAIR_REGISTRY.get_or_init(|| Mutex::new(HashMap::new()))
}

fn parallel_direction_factor_midpoint(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> Option<(i64, i64)> {
    let (_det_value, _other_leg, _scaled_hypotenuse, _second_length, first_coefficient) =
        parallel_direction_factor_witness_data_i128(target, direction, factor)?;
    if first_coefficient == 0 {
        return None;
    }
    let u = direction.0 as i128;
    let v = direction.1 as i128;
    let midpoint = (
        i128_to_i64(first_coefficient * u)?,
        i128_to_i64(first_coefficient * v)?,
    );
    if certificate_valid(target, midpoint) {
        Some(midpoint)
    } else {
        None
    }
}

fn parallel_direction_factor_witness_data_i128(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> Option<(i128, i128, i128, i128, i128)> {
    let (det_value, _paired_factor, other_leg, scaled_hypotenuse, second_length, first_coefficient) =
        parallel_direction_factor_witness_row_data_i128(target, direction, factor)?;
    Some((
        det_value,
        other_leg,
        scaled_hypotenuse,
        second_length,
        first_coefficient,
    ))
}

fn parallel_direction_factor_witness_row_data_i128(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> Option<(i128, i128, i128, i128, i128, i128)> {
    let u = direction.0 as i128;
    let v = direction.1 as i128;
    let c = isqrt_i128(u * u + v * v);
    let det_value = determinant(direction, target);
    if det_value == 0 {
        return None;
    }
    let determinant_square = det_value * det_value;
    let factor = factor as i128;
    if determinant_square % factor != 0 {
        return None;
    }
    let paired_factor = determinant_square / factor;
    let factor_sum = factor + paired_factor;
    let factor_difference = paired_factor - factor;
    if factor_sum % (2 * c) != 0 || factor_difference % 2 != 0 {
        return None;
    }
    let other_leg = factor_difference / 2;
    let dot_product = target.0 as i128 * u + target.1 as i128 * v;
    let first_coefficient_numerator = other_leg + dot_product;
    let direction_norm = c * c;
    if first_coefficient_numerator % direction_norm != 0 {
        return None;
    }
    let first_coefficient = first_coefficient_numerator / direction_norm;
    let scaled_hypotenuse = factor_sum / 2;
    Some((
        det_value,
        paired_factor,
        other_leg,
        scaled_hypotenuse,
        scaled_hypotenuse / c,
        first_coefficient,
    ))
}

#[pyfunction]
fn parallel_direction_factor_witness_data(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Option<(i128, i128, i128, i128, i128)>> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }
    Ok(parallel_direction_factor_witness_data_i128(
        target, direction, factor,
    ))
}

#[pyfunction]
fn parallel_direction_factor_witness_row_data(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Option<(i128, i128, i128, i128, i128, i128)>> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }
    Ok(parallel_direction_factor_witness_row_data_i128(
        target, direction, factor,
    ))
}

fn parallel_direction_certificate_midpoint_inner(
    target: (i64, i64),
    direction: (i64, i64),
) -> Option<(i64, i64)> {
    let det_value = determinant(direction, target);
    if det_value == 0 {
        return None;
    }
    let determinant_square = (det_value.abs() * det_value.abs()) as u64;
    for factor in positive_divisors_vec(determinant_square) {
        if let Some(midpoint) = parallel_direction_factor_midpoint(target, direction, factor as i64)
        {
            return Some(midpoint);
        }
    }
    None
}

fn signed_swap_point_inner(point: (i64, i64), x_sign: i64, y_sign: i64, swap: bool) -> (i64, i64) {
    let (x, y) = if swap { (point.1, point.0) } else { point };
    (x_sign * x, y_sign * y)
}

fn signed_swap_point_i128(
    point: (i128, i128),
    x_sign: i64,
    y_sign: i64,
    swap: bool,
) -> (i128, i128) {
    let (x, y) = if swap { (point.1, point.0) } else { point };
    (x_sign as i128 * x, y_sign as i128 * y)
}

#[pyfunction]
fn edge_delta(dx: i64, dy: i64) -> bool {
    edge_delta_i128(dx as i128, dy as i128)
}

#[pyfunction]
fn certificate_valid(target: (i64, i64), midpoint: (i64, i64)) -> bool {
    certificate_valid_i128(
        (target.0 as i128, target.1 as i128),
        (midpoint.0 as i128, midpoint.1 as i128),
    )
}

#[pyfunction]
fn scale_certificate_data(
    certificate_target: (i64, i64),
    certificate_midpoint: (i64, i64),
    factor: i64,
) -> PyResult<((i128, i128), (i128, i128))> {
    if factor == 0 {
        return Err(PyValueError::new_err(
            "certificate scaling factor must be nonzero",
        ));
    }

    let factor = factor as i128;
    Ok((
        (
            factor * certificate_target.0 as i128,
            factor * certificate_target.1 as i128,
        ),
        (
            factor * certificate_midpoint.0 as i128,
            factor * certificate_midpoint.1 as i128,
        ),
    ))
}

#[pyfunction(signature = (certificate_target, certificate_midpoint, factor, x_sign, y_sign, swap=false))]
fn scale_signed_swap_certificate_data(
    certificate_target: (i64, i64),
    certificate_midpoint: (i64, i64),
    factor: i64,
    x_sign: i64,
    y_sign: i64,
    swap: bool,
) -> PyResult<((i128, i128), (i128, i128))> {
    if factor == 0 {
        return Err(PyValueError::new_err(
            "certificate scaling factor must be nonzero",
        ));
    }
    if ![-1, 1].contains(&x_sign) || ![-1, 1].contains(&y_sign) {
        return Err(PyValueError::new_err("x_sign and y_sign must be -1 or 1"));
    }

    let factor = factor as i128;
    let target = (
        factor * certificate_target.0 as i128,
        factor * certificate_target.1 as i128,
    );
    let midpoint = (
        factor * certificate_midpoint.0 as i128,
        factor * certificate_midpoint.1 as i128,
    );
    Ok((
        signed_swap_point_i128(target, x_sign, y_sign, swap),
        signed_swap_point_i128(midpoint, x_sign, y_sign, swap),
    ))
}

fn pythagorean_leg_completion_i128(leg: i128) -> Option<(i128, i128)> {
    if leg < 3 {
        return None;
    }
    if leg % 2 != 0 {
        Some(((leg * leg - 1) / 2, (leg * leg + 1) / 2))
    } else {
        let half = leg / 2;
        Some((half * half - 1, half * half + 1))
    }
}

#[pyfunction]
fn even_axis_certificate_midpoint(n: i64) -> Option<(i128, i128)> {
    if n < 6 || n % 2 != 0 {
        return None;
    }
    let half = n as i128 / 2;
    let (partner_leg, _hypotenuse) = pythagorean_leg_completion_i128(half)?;
    Some((half, partner_leg))
}

#[pyfunction]
fn consecutive_odd_axis_certificate_data(
    n: i64,
) -> PyResult<Option<(i128, i128, i128, i128, i128, i128, i128, i128)>> {
    if n < 3 || n % 2 == 0 {
        return Ok(None);
    }

    let n = n as i128;
    let first_scale = (n - 1) / 2;
    let second_scale = (n + 1) / 2;
    let two_n = checked_axis_mul(2, n)?;
    let n_square = checked_axis_mul(n, n)?;
    let shared_leg = checked_axis_mul(n, checked_axis_sub(n_square, 1)?)?;
    let first_horizontal_leg = checked_axis_mul(first_scale, checked_axis_add(two_n, 1)?)?;
    let second_horizontal_leg = checked_axis_mul(second_scale, checked_axis_sub(two_n, 1)?)?;
    let first_hypotenuse = checked_axis_mul(
        first_scale,
        checked_axis_add(checked_axis_add(checked_axis_mul(2, n_square)?, two_n)?, 1)?,
    )?;
    let second_hypotenuse = checked_axis_mul(
        second_scale,
        checked_axis_add(checked_axis_sub(checked_axis_mul(2, n_square)?, two_n)?, 1)?,
    )?;
    let target_n = checked_axis_sub(second_horizontal_leg, first_horizontal_leg)?;

    Ok(Some((
        target_n,
        -first_horizontal_leg,
        shared_leg,
        shared_leg,
        first_horizontal_leg,
        second_horizontal_leg,
        first_hypotenuse,
        second_hypotenuse,
    )))
}

fn gaussian_multiply_i128(point: (i128, i128), multiplier: (i128, i128)) -> (i128, i128) {
    let (x, y) = point;
    let (a, b) = multiplier;
    (x * a - y * b, x * b + y * a)
}

#[pyfunction]
fn gaussian_multiply(point: (i64, i64), multiplier: (i64, i64)) -> (i128, i128) {
    gaussian_multiply_i128(
        (point.0 as i128, point.1 as i128),
        (multiplier.0 as i128, multiplier.1 as i128),
    )
}

#[pyfunction]
fn gaussian_transform_certificate_data(
    certificate_target: (i64, i64),
    certificate_midpoint: (i64, i64),
    multiplier: (i64, i64),
) -> PyResult<Option<((i128, i128), (i128, i128))>> {
    if !certificate_valid(certificate_target, certificate_midpoint) {
        return Err(PyValueError::new_err(
            "certificate must be valid before transformation",
        ));
    }

    let multiplier_i128 = (multiplier.0 as i128, multiplier.1 as i128);
    let multiplier_norm =
        multiplier_i128.0 * multiplier_i128.0 + multiplier_i128.1 * multiplier_i128.1;
    if multiplier_norm == 0 || !is_square_i128(multiplier_norm) {
        return Err(PyValueError::new_err(
            "Gaussian multiplier must have nonzero square norm",
        ));
    }

    let target = gaussian_multiply_i128(
        (certificate_target.0 as i128, certificate_target.1 as i128),
        multiplier_i128,
    );
    let midpoint = gaussian_multiply_i128(
        (
            certificate_midpoint.0 as i128,
            certificate_midpoint.1 as i128,
        ),
        multiplier_i128,
    );
    if certificate_valid_i128(target, midpoint) {
        Ok(Some((target, midpoint)))
    } else {
        Ok(None)
    }
}

fn gaussian_quotient_components_i128(
    target: (i128, i128),
    divisor: (i128, i128),
) -> PyResult<(i128, i128, i128)> {
    let divisor_norm = divisor.0 * divisor.0 + divisor.1 * divisor.1;
    if divisor_norm == 0 {
        return Err(PyValueError::new_err("Gaussian divisor must be nonzero"));
    }

    Ok((
        target.0 * divisor.0 + target.1 * divisor.1,
        target.1 * divisor.0 - target.0 * divisor.1,
        divisor_norm,
    ))
}

#[pyfunction]
fn gaussian_quotient_components(
    target: (i64, i64),
    divisor: (i64, i64),
) -> PyResult<(i128, i128, i128)> {
    gaussian_quotient_components_i128(
        (target.0 as i128, target.1 as i128),
        (divisor.0 as i128, divisor.1 as i128),
    )
}

#[pyfunction]
fn gaussian_quotient_if_integer(
    target: (i64, i64),
    divisor: (i64, i64),
) -> PyResult<Option<(i128, i128)>> {
    let (real_numerator, imaginary_numerator, divisor_norm) = gaussian_quotient_components_i128(
        (target.0 as i128, target.1 as i128),
        (divisor.0 as i128, divisor.1 as i128),
    )?;
    if real_numerator % divisor_norm != 0 || imaginary_numerator % divisor_norm != 0 {
        return Ok(None);
    }
    Ok(Some((
        real_numerator / divisor_norm,
        imaginary_numerator / divisor_norm,
    )))
}

#[pyfunction]
fn gaussian_divisor_certificate_midpoint(
    target: (i64, i64),
    base_target: (i64, i64),
    base_midpoint: (i64, i64),
) -> PyResult<Option<(i128, i128)>> {
    if !certificate_valid(base_target, base_midpoint) {
        return Err(PyValueError::new_err("base certificate must be valid"));
    }

    let Some(multiplier) = gaussian_quotient_if_integer(target, base_target)? else {
        return Ok(None);
    };
    let multiplier_norm = multiplier.0 * multiplier.0 + multiplier.1 * multiplier.1;
    if multiplier_norm == 0 || !is_square_i128(multiplier_norm) {
        return Ok(None);
    }

    let target_i128 = (target.0 as i128, target.1 as i128);
    let midpoint = gaussian_multiply_i128(
        (base_midpoint.0 as i128, base_midpoint.1 as i128),
        multiplier,
    );
    if certificate_valid_i128(target_i128, midpoint) {
        Ok(Some(midpoint))
    } else {
        Ok(None)
    }
}

#[pyfunction]
fn diagonal_pythagorean_multiplier_midpoint(target: (i64, i64)) -> Option<(i128, i128)> {
    let target_i128 = (target.0 as i128, target.1 as i128);
    let sum = target_i128.0 + target_i128.1;
    let difference = target_i128.1 - target_i128.0;
    if sum % 2 != 0 || difference % 2 != 0 {
        return None;
    }

    let multiplier = (sum / 2, difference / 2);
    let multiplier_norm = multiplier.0 * multiplier.0 + multiplier.1 * multiplier.1;
    if multiplier_norm == 0 || !is_square_i128(multiplier_norm) {
        return None;
    }

    let midpoint = gaussian_multiply_i128((4, -3), multiplier);
    if certificate_valid_i128(target_i128, midpoint) {
        Some(midpoint)
    } else {
        None
    }
}

#[pyfunction]
fn theorem3_certificate_midpoint(
    target: (i64, i64),
    triple: (i64, i64, i64),
    x_sign: i64,
    y_sign: i64,
) -> PyResult<Option<(i128, i128)>> {
    theorem3_midpoint_i128(target, triple, x_sign, y_sign, 1, false, true)
}

#[pyfunction]
fn theorem3_divisor_certificate_midpoint(
    target: (i64, i64),
    triple: (i64, i64, i64),
    x_sign: i64,
    y_sign: i64,
    divisor: i64,
) -> PyResult<Option<(i128, i128)>> {
    theorem3_midpoint_i128(target, triple, x_sign, y_sign, divisor as i128, true, false)
}

#[pyfunction]
fn linear_delta_direction_midpoint(
    target: (i64, i64),
    direction: (i64, i64),
    delta_coefficients: (i64, i64),
) -> PyResult<Option<(i128, i128)>> {
    linear_delta_direction_midpoint_i128(target, direction, delta_coefficients)
}

#[pyfunction(signature = (point, x_sign, y_sign, swap=false))]
fn signed_swap_point(
    point: (i64, i64),
    x_sign: i64,
    y_sign: i64,
    swap: bool,
) -> PyResult<(i64, i64)> {
    if ![-1, 1].contains(&x_sign) || ![-1, 1].contains(&y_sign) {
        return Err(PyValueError::new_err("x_sign and y_sign must be -1 or 1"));
    }
    Ok(signed_swap_point_inner(point, x_sign, y_sign, swap))
}

#[pyfunction]
fn sign_swap_certificate_midpoint(
    certificate_target: (i64, i64),
    certificate_midpoint: (i64, i64),
    target: (i64, i64),
) -> PyResult<Option<(i64, i64)>> {
    for swap in [false, true] {
        for x_sign in [-1, 1] {
            for y_sign in [-1, 1] {
                let transformed_target =
                    signed_swap_point_inner(certificate_target, x_sign, y_sign, swap);
                if transformed_target != target {
                    continue;
                }

                let transformed_midpoint =
                    signed_swap_point_inner(certificate_midpoint, x_sign, y_sign, swap);
                if !certificate_valid(target, transformed_midpoint) {
                    return Err(PyAssertionError::new_err(
                        "sign/swap transform produced an invalid certificate",
                    ));
                }
                return Ok(Some(transformed_midpoint));
            }
        }
    }
    Ok(None)
}

#[pyfunction]
fn lattice_coefficients(
    target: (i64, i64),
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> Option<(i128, i128)> {
    lattice_coefficients_i128(target, first_direction, second_direction)
}

#[pyfunction]
fn lattice_coefficient_cramer_data(
    target: (i64, i64),
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> PyResult<(i128, i128, i128, bool, bool, Option<i128>, Option<i128>)> {
    let determinant_value = determinant(first_direction, second_direction);
    if determinant_value == 0 {
        return Err(PyValueError::new_err(
            "lattice directions must be independent",
        ));
    }

    let first_numerator = target.0 as i128 * second_direction.1 as i128
        - target.1 as i128 * second_direction.0 as i128;
    let second_numerator =
        first_direction.0 as i128 * target.1 as i128 - first_direction.1 as i128 * target.0 as i128;
    let first_divisible = first_numerator % determinant_value == 0;
    let second_divisible = second_numerator % determinant_value == 0;
    Ok((
        determinant_value,
        first_numerator,
        second_numerator,
        first_divisible,
        second_divisible,
        first_divisible.then_some(first_numerator / determinant_value),
        second_divisible.then_some(second_numerator / determinant_value),
    ))
}

#[pyfunction]
fn lattice_certificate_midpoint(
    target: (i64, i64),
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> PyResult<Option<(i128, i128)>> {
    if !edge_delta(first_direction.0, first_direction.1)
        || !edge_delta(second_direction.0, second_direction.1)
    {
        return Err(PyValueError::new_err(
            "directions must be legal Pythagorean edge vectors",
        ));
    }
    lattice_certificate_midpoint_i128(target, first_direction, second_direction)
}

#[pyfunction]
fn gaussian_root_conjugate_divisibility_residue(root: (i64, i64)) -> PyResult<(i128, i128)> {
    if root.0 == 0 || root.1 == 0 {
        return Err(PyValueError::new_err("root coordinates must be nonzero"));
    }
    if gcd_i128(root.0 as i128, root.1 as i128) != 1 {
        return Err(PyValueError::new_err("root must be primitive"));
    }

    let root_real = root.0 as i128;
    let root_imaginary = root.1 as i128;
    let hypotenuse = root_real * root_real + root_imaginary * root_imaginary;
    let Some(inverse) = modular_inverse_i128(root_real, hypotenuse) else {
        return Err(PyValueError::new_err("root must be primitive"));
    };
    let residue = mul_mod_i128(-root_imaginary, inverse, hypotenuse);
    if (mul_mod_i128(residue, residue, hypotenuse) + 1) % hypotenuse != 0 {
        return Err(PyAssertionError::new_err(
            "conjugate-root residue is not a square root of -1",
        ));
    }
    Ok((hypotenuse, residue))
}

#[pyfunction]
fn prime_power_factorization(n: u64) -> PyResult<Vec<(u64, u32)>> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be positive"));
    }
    Ok(factorize(n))
}

#[pyfunction]
fn prime_factors(n: u64) -> PyResult<Vec<u64>> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be positive"));
    }
    Ok(factorize(n).into_iter().map(|(prime, _)| prime).collect())
}

#[pyfunction]
fn positive_divisors(n: u64) -> PyResult<Vec<u64>> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be positive"));
    }
    Ok(positive_divisors_vec(n))
}

#[pyfunction]
fn divisor_residue_classes(n: u64, modulus: u64) -> PyResult<Vec<u64>> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be positive"));
    }
    if modulus == 0 {
        return Err(PyValueError::new_err("modulus must be positive"));
    }
    Ok(divisor_residue_classes_vec(n, modulus))
}

#[pyfunction]
fn has_divisor_in_residue_classes(n: u64, modulus: u64, residues: Vec<i64>) -> PyResult<bool> {
    if n == 0 {
        return Err(PyValueError::new_err("n must be positive"));
    }
    if modulus == 0 {
        return Err(PyValueError::new_err("modulus must be positive"));
    }
    let wanted: BTreeSet<u64> = residues
        .into_iter()
        .map(|residue| residue.rem_euclid(modulus as i64) as u64)
        .collect();
    Ok(divisor_residue_classes_vec(n, modulus)
        .into_iter()
        .any(|residue| wanted.contains(&residue)))
}

#[pyfunction]
fn parallel_direction_factor_modulus(direction: (i64, i64), factor: i64) -> PyResult<i64> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }
    Ok(2 * (direction.0 * direction.0 + direction.1 * direction.1) * factor)
}

#[pyfunction]
fn parallel_direction_factor_congruence_holds(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> PyResult<bool> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }
    Ok(factor_congruence_holds(target, direction, factor))
}

#[pyfunction]
fn parallel_direction_factor_congruence_data(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Option<(i128, i128, i128)>> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }
    parallel_direction_factor_congruence_data_i128(target, direction, factor)
}

#[pyfunction]
fn parallel_direction_factor_pair_row_from_congruence_data(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Option<(i128, i128, i128, i128, i128, i128)>> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }

    let Some((determinant_leg, second_length, first_coefficient)) =
        parallel_direction_factor_congruence_data_i128(target, direction, factor)?
    else {
        return Ok(None);
    };
    let factor = factor as i128;
    let determinant_square = checked_parallel_factor_mul(determinant_leg, determinant_leg)?;
    if determinant_square % factor != 0 {
        return Ok(None);
    }

    let paired_factor = determinant_square / factor;
    let u = direction.0 as i128;
    let v = direction.1 as i128;
    let c = isqrt_i128(checked_parallel_factor_add(
        checked_parallel_factor_mul(u, u)?,
        checked_parallel_factor_mul(v, v)?,
    )?);
    let scaled_hypotenuse = checked_parallel_factor_mul(c, second_length)?;
    if checked_parallel_factor_add(factor, paired_factor)?
        != checked_parallel_factor_mul(2, scaled_hypotenuse)?
    {
        return Err(PyAssertionError::new_err(
            "congruence data did not recover the factor-pair sum",
        ));
    }

    let target_x = target.0 as i128;
    let target_y = target.1 as i128;
    let dot_product = checked_parallel_factor_add(
        checked_parallel_factor_mul(target_x, u)?,
        checked_parallel_factor_mul(target_y, v)?,
    )?;
    let difference = checked_parallel_factor_sub(paired_factor, factor)?;
    let coefficient_lhs =
        checked_parallel_factor_add(difference, checked_parallel_factor_mul(2, dot_product)?)?;
    let c_square = checked_parallel_factor_mul(c, c)?;
    let coefficient_rhs =
        checked_parallel_factor_mul(checked_parallel_factor_mul(2, first_coefficient)?, c_square)?;
    if coefficient_lhs != coefficient_rhs {
        return Err(PyAssertionError::new_err(
            "congruence data did not recover the coefficient row",
        ));
    }
    if difference % 2 != 0 {
        return Err(PyAssertionError::new_err(
            "factor-pair difference must be even",
        ));
    }

    Ok(Some((
        determinant_leg,
        paired_factor,
        difference / 2,
        scaled_hypotenuse,
        second_length,
        first_coefficient,
    )))
}

#[pyfunction]
fn parallel_direction_primitive_factor_determinant_residue_rows(
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Vec<(i128, i128)>> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if gcd_i128(direction.0 as i128, direction.1 as i128) != 1 {
        return Err(PyValueError::new_err("direction must be primitive"));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }
    primitive_factor_determinant_residue_rows_i128(direction, factor)
}

#[pyfunction]
fn ray_parallel_factor_residues(
    ray: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Vec<i64>> {
    if ray.0 == 0 && ray.1 == 0 {
        return Err(PyValueError::new_err("ray must be nonzero"));
    }
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    if factor <= 0 {
        return Err(PyValueError::new_err("factor must be positive"));
    }

    let direction_norm =
        direction.0 as i128 * direction.0 as i128 + direction.1 as i128 * direction.1 as i128;
    let c = isqrt_i128(direction_norm);
    let modulus = 2_i128 * direction_norm * factor as i128;
    let ray_determinant = determinant(direction, ray);
    if ray_determinant == 0 {
        return Ok(Vec::new());
    }
    let ray_dot = ray.0 as i128 * direction.0 as i128 + ray.1 as i128 * direction.1 as i128;
    let mut residues = Vec::new();
    let mut residue = 0_i128;
    while residue < modulus {
        let multiplier = if residue == 0 { modulus } else { residue };
        let det_value = multiplier * ray_determinant;
        let determinant_square = det_value * det_value;
        if determinant_square % factor as i128 == 0 {
            let paired_factor = determinant_square / factor as i128;
            let factor_sum = factor as i128 + paired_factor;
            let factor_difference = paired_factor - factor as i128;
            if factor_sum % (2 * c) == 0 && factor_difference % 2 == 0 {
                let other_leg = factor_difference / 2;
                let dot_product = multiplier * ray_dot;
                let first_coefficient_numerator = other_leg + dot_product;
                if first_coefficient_numerator % direction_norm == 0 {
                    residues.push(residue as i64);
                }
            }
        }
        residue += 1;
    }
    Ok(residues)
}

#[pyfunction]
fn parallel_direction_factor_residue_classes(
    direction: (i64, i64),
    factor: i64,
) -> PyResult<Vec<(i64, i64)>> {
    let modulus = parallel_direction_factor_modulus(direction, factor)?;
    let mut residues = Vec::new();
    for g in 0..modulus {
        for h in 0..modulus {
            if factor_congruence_holds((g, h), direction, factor) {
                residues.push((g, h));
            }
        }
    }
    Ok(residues)
}

#[pyfunction]
fn parallel_direction_factor_integrality_strip_intersection_residue_count(
    strip_direction: (i64, i64),
    strip_modulus: i64,
    strip_residue: i64,
    factor_direction: (i64, i64),
    factor: i64,
) -> PyResult<(i64, i64)> {
    if !edge_delta(strip_direction.0, strip_direction.1) {
        return Err(PyValueError::new_err(
            "strip direction must be a legal Pythagorean edge vector",
        ));
    }
    if strip_modulus <= 1 {
        return Err(PyValueError::new_err(
            "strip modulus must be greater than 1",
        ));
    }
    let factor_modulus = parallel_direction_factor_modulus(factor_direction, factor)?;
    let shared_modulus = gcd_i128(factor_modulus as i128, strip_modulus as i128) as i64;
    let lift_count = strip_modulus / shared_modulus;
    let lcm_modulus = factor_modulus * lift_count;
    let shared = shared_modulus as i128;
    let strip_residue = strip_residue as i128;
    let mut compatible = 0_i64;
    for g in 0..factor_modulus {
        for h in 0..factor_modulus {
            let point = (g, h);
            if !factor_congruence_holds(point, factor_direction, factor) {
                continue;
            }
            if (determinant(strip_direction, point) - strip_residue) % shared == 0 {
                compatible += 1;
            }
        }
    }
    Ok((lcm_modulus, compatible * lift_count))
}

#[pyfunction]
fn pythagorean_lattice_pair_strip_linear_congruence(
    strip_direction: (i64, i64),
    strip_modulus: i64,
    strip_residue: i64,
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> PyResult<(i128, i128, i128, i128, i128)> {
    if !edge_delta(strip_direction.0, strip_direction.1) {
        return Err(PyValueError::new_err(
            "strip direction must be a legal Pythagorean edge vector",
        ));
    }
    if strip_modulus <= 1 {
        return Err(PyValueError::new_err(
            "strip modulus must be greater than 1",
        ));
    }
    if !edge_delta(first_direction.0, first_direction.1)
        || !edge_delta(second_direction.0, second_direction.1)
    {
        return Err(PyValueError::new_err(
            "lattice directions must be legal Pythagorean edge vectors",
        ));
    }
    if determinant(first_direction, second_direction) == 0 {
        return Err(PyValueError::new_err(
            "lattice directions must be independent",
        ));
    }

    let modulus = strip_modulus as i128;
    let strip = (strip_direction.0 as i128, strip_direction.1 as i128);
    let first = (first_direction.0 as i128, first_direction.1 as i128);
    let second = (second_direction.0 as i128, second_direction.1 as i128);
    let first_step = determinant_i128(strip, first).rem_euclid(modulus);
    let second_step = determinant_i128(strip, second).rem_euclid(modulus);
    let residue = (strip_residue as i128).rem_euclid(modulus);
    let linear_gcd = gcd_i128(gcd_i128(first_step, second_step), modulus);
    Ok((first_step, second_step, residue, modulus, linear_gcd))
}

#[pyfunction]
fn two_variable_linear_congruence_gcd(
    first_step: i64,
    second_step: i64,
    residue: i64,
    modulus: i64,
) -> PyResult<(i128, bool)> {
    if modulus <= 0 {
        return Err(PyValueError::new_err("modulus must be positive"));
    }

    let linear_gcd = gcd_i128(
        gcd_i128(first_step as i128, second_step as i128),
        modulus as i128,
    );
    Ok((linear_gcd, (residue as i128) % linear_gcd == 0))
}

fn two_variable_linear_congruence_pair_data_i128(
    first_step: i128,
    second_step: i128,
    first_residue: i128,
    first_modulus: i128,
    second_residue: i128,
    second_modulus: i128,
) -> PyResult<(i128, i128, i128, Option<i128>, bool, bool)> {
    if first_modulus <= 0 || second_modulus <= 0 {
        return Err(PyValueError::new_err("moduli must be positive"));
    }

    let shared_modulus = gcd_i128(first_modulus, second_modulus);
    let lcm_modulus = (first_modulus / shared_modulus) * second_modulus;
    let linear_gcd = gcd_i128(gcd_i128(first_step, second_step), lcm_modulus);
    let first_residue = first_residue.rem_euclid(first_modulus);
    let second_residue = second_residue.rem_euclid(second_modulus);
    let residues_compatible = (first_residue - second_residue).rem_euclid(shared_modulus) == 0;
    if !residues_compatible {
        return Ok((shared_modulus, lcm_modulus, linear_gcd, None, false, false));
    }

    let first_coprime_part = first_modulus / shared_modulus;
    let second_coprime_part = second_modulus / shared_modulus;
    let quotient_residue = (second_residue - first_residue) / shared_modulus;
    let Some(inverse) = modular_inverse_i128(first_coprime_part, second_coprime_part) else {
        return Err(PyValueError::new_err("reduced moduli must be coprime"));
    };
    let lift = mul_mod_i128(quotient_residue, inverse, second_coprime_part);
    let combined_residue = (first_residue + first_modulus * lift).rem_euclid(lcm_modulus);
    Ok((
        shared_modulus,
        lcm_modulus,
        linear_gcd,
        Some(combined_residue),
        true,
        combined_residue % linear_gcd == 0,
    ))
}

#[pyfunction]
fn two_variable_linear_congruence_pair_data(
    first_step: i64,
    second_step: i64,
    first_residue: i64,
    first_modulus: i64,
    second_residue: i64,
    second_modulus: i64,
) -> PyResult<(i128, i128, i128, Option<i128>, bool, bool)> {
    two_variable_linear_congruence_pair_data_i128(
        first_step as i128,
        second_step as i128,
        first_residue as i128,
        first_modulus as i128,
        second_residue as i128,
        second_modulus as i128,
    )
}

#[pyfunction]
fn pythagorean_lattice_pair_strip_crt_data(
    strip_direction: (i64, i64),
    first_modulus: i64,
    first_residue: i64,
    second_modulus: i64,
    second_residue: i64,
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> PyResult<(i128, i128, i128, i128, i128, Option<i128>, bool, bool)> {
    if !edge_delta(strip_direction.0, strip_direction.1) {
        return Err(PyValueError::new_err(
            "strip direction must be a legal Pythagorean edge vector",
        ));
    }
    if first_modulus <= 1 || second_modulus <= 1 {
        return Err(PyValueError::new_err("strip moduli must be greater than 1"));
    }
    if !edge_delta(first_direction.0, first_direction.1)
        || !edge_delta(second_direction.0, second_direction.1)
    {
        return Err(PyValueError::new_err(
            "lattice directions must be legal Pythagorean edge vectors",
        ));
    }
    if determinant(first_direction, second_direction) == 0 {
        return Err(PyValueError::new_err(
            "lattice directions must be independent",
        ));
    }

    let strip = (strip_direction.0 as i128, strip_direction.1 as i128);
    let first = (first_direction.0 as i128, first_direction.1 as i128);
    let second = (second_direction.0 as i128, second_direction.1 as i128);
    let first_step = determinant_i128(strip, first);
    let second_step = determinant_i128(strip, second);
    let (shared_modulus, lcm_modulus, linear_gcd, combined_residue, compatible, solvable) =
        two_variable_linear_congruence_pair_data_i128(
            first_step,
            second_step,
            first_residue as i128,
            first_modulus as i128,
            second_residue as i128,
            second_modulus as i128,
        )?;
    Ok((
        first_step,
        second_step,
        shared_modulus,
        lcm_modulus,
        linear_gcd,
        combined_residue,
        compatible,
        solvable,
    ))
}

#[pyfunction]
fn pythagorean_lattice_pair_same_strip_combined_linear_congruence(
    strip_direction: (i64, i64),
    first_modulus: i64,
    first_residue: i64,
    second_modulus: i64,
    second_residue: i64,
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> PyResult<Option<(i128, i128, i128, i128, i128)>> {
    let (
        first_step,
        second_step,
        _shared_modulus,
        lcm_modulus,
        linear_gcd,
        combined_residue,
        compatible,
        _solvable,
    ) = pythagorean_lattice_pair_strip_crt_data(
        strip_direction,
        first_modulus,
        first_residue,
        second_modulus,
        second_residue,
        first_direction,
        second_direction,
    )?;
    if !compatible {
        return Ok(None);
    }
    let combined_residue = combined_residue
        .ok_or_else(|| PyValueError::new_err("compatible CRT row has no combined residue"))?;
    Ok(Some((
        first_step.rem_euclid(lcm_modulus),
        second_step.rem_euclid(lcm_modulus),
        combined_residue,
        lcm_modulus,
        linear_gcd,
    )))
}

fn checked_count_mul(left: i128, right: i128) -> PyResult<i128> {
    left.checked_mul(right)
        .ok_or_else(|| PyOverflowError::new_err("lattice strip count exceeded i128"))
}

#[pyfunction]
fn pythagorean_lattice_pair_same_strip_intersection_residue_count(
    strip_direction: (i64, i64),
    first_modulus: i64,
    first_residue: i64,
    second_modulus: i64,
    second_residue: i64,
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> PyResult<(i128, i128)> {
    let (
        _first_step,
        _second_step,
        _shared_modulus,
        row_modulus,
        linear_gcd,
        _combined_residue,
        compatible,
        solvable,
    ) = pythagorean_lattice_pair_strip_crt_data(
        strip_direction,
        first_modulus,
        first_residue,
        second_modulus,
        second_residue,
        first_direction,
        second_direction,
    )?;
    let pair_determinant = determinant(first_direction, second_direction).abs();
    let shared_modulus = gcd_i128(pair_determinant, row_modulus);
    let target_modulus = checked_count_mul(pair_determinant / shared_modulus, row_modulus)?;
    if !compatible || !solvable {
        return Ok((target_modulus, 0));
    }

    let numerator = checked_count_mul(
        checked_count_mul(target_modulus, target_modulus)?,
        linear_gcd,
    )?;
    let denominator = checked_count_mul(row_modulus, pair_determinant)?;
    Ok((target_modulus, numerator / denominator))
}

#[pyfunction(signature = (target, max_parameter, max_determinant=None))]
fn pythagorean_lattice_pair_witness(
    target: (i64, i64),
    max_parameter: i64,
    max_determinant: Option<i64>,
) -> PyResult<Option<((i64, i64), (i64, i64), i64, i64, i64)>> {
    if max_parameter < 2 {
        return Err(PyValueError::new_err("max_parameter must be at least 2"));
    }
    if max_determinant.is_some_and(|limit| limit <= 0) {
        return Err(PyValueError::new_err("max_determinant must be positive"));
    }
    if max_parameter == 25 && max_determinant == Some(1435) {
        let pairs = LATTICE_PAIRS_25_1435.get_or_init(|| generate_lattice_pairs(25, Some(1435)));
        return Ok(lattice_pair_witness_from_pairs(target, pairs));
    }
    let pairs = generate_lattice_pairs(max_parameter, max_determinant);
    Ok(lattice_pair_witness_from_pairs(target, &pairs))
}

#[pyfunction]
fn parallel_direction_certificate_midpoint(
    target: (i64, i64),
    direction: (i64, i64),
) -> PyResult<Option<(i64, i64)>> {
    if !edge_delta(direction.0, direction.1) {
        return Err(PyValueError::new_err(
            "direction must be a legal Pythagorean edge vector",
        ));
    }
    Ok(parallel_direction_certificate_midpoint_inner(
        target, direction,
    ))
}

#[pyfunction]
fn parallel_direction_cover_midpoint(
    target: (i64, i64),
    max_parameter: i64,
) -> PyResult<Option<(i64, i64)>> {
    if max_parameter < 2 {
        return Err(PyValueError::new_err("max_parameter must be at least 2"));
    }
    for (u, v, _hypotenuse) in primitive_pythagorean_directions(max_parameter) {
        if let Some(midpoint) = parallel_direction_certificate_midpoint_inner(target, (u, v)) {
            return Ok(Some(midpoint));
        }
    }
    Ok(None)
}

#[pyfunction]
fn register_lattice_pairs(
    name: String,
    direction_pairs: Vec<((i64, i64), (i64, i64))>,
) -> PyResult<()> {
    let pairs = direction_pairs
        .into_iter()
        .map(|(first, second)| LatticePair {
            first,
            second,
            determinant: determinant(first, second).abs() as i64,
        })
        .collect();
    registered_lattice_pairs()
        .lock()
        .expect("lattice registry lock poisoned")
        .insert(name, pairs);
    Ok(())
}

#[pyfunction]
fn first_registered_lattice_midpoint(
    name: String,
    target: (i64, i64),
) -> PyResult<Option<(i64, i64)>> {
    let registry = registered_lattice_pairs()
        .lock()
        .expect("lattice registry lock poisoned");
    let Some(pairs) = registry.get(&name) else {
        return Err(PyValueError::new_err("unknown lattice pair table"));
    };
    Ok(lattice_pair_witness_from_pairs(target, pairs).map(
        |(first, _second, _determinant, first_coefficient, _second_coefficient)| {
            (first_coefficient * first.0, first_coefficient * first.1)
        },
    ))
}

#[pymodule]
fn pythagorean_walks_fast(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(edge_delta, m)?)?;
    m.add_function(wrap_pyfunction!(certificate_valid, m)?)?;
    m.add_function(wrap_pyfunction!(scale_certificate_data, m)?)?;
    m.add_function(wrap_pyfunction!(scale_signed_swap_certificate_data, m)?)?;
    m.add_function(wrap_pyfunction!(even_axis_certificate_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(consecutive_odd_axis_certificate_data, m)?)?;
    m.add_function(wrap_pyfunction!(gaussian_multiply, m)?)?;
    m.add_function(wrap_pyfunction!(gaussian_transform_certificate_data, m)?)?;
    m.add_function(wrap_pyfunction!(gaussian_quotient_components, m)?)?;
    m.add_function(wrap_pyfunction!(gaussian_quotient_if_integer, m)?)?;
    m.add_function(wrap_pyfunction!(gaussian_divisor_certificate_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(
        diagonal_pythagorean_multiplier_midpoint,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(theorem3_certificate_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(theorem3_divisor_certificate_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(linear_delta_direction_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(signed_swap_point, m)?)?;
    m.add_function(wrap_pyfunction!(sign_swap_certificate_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(lattice_coefficients, m)?)?;
    m.add_function(wrap_pyfunction!(lattice_coefficient_cramer_data, m)?)?;
    m.add_function(wrap_pyfunction!(lattice_certificate_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(
        gaussian_root_conjugate_divisibility_residue,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(prime_power_factorization, m)?)?;
    m.add_function(wrap_pyfunction!(prime_factors, m)?)?;
    m.add_function(wrap_pyfunction!(positive_divisors, m)?)?;
    m.add_function(wrap_pyfunction!(divisor_residue_classes, m)?)?;
    m.add_function(wrap_pyfunction!(has_divisor_in_residue_classes, m)?)?;
    m.add_function(wrap_pyfunction!(parallel_direction_factor_modulus, m)?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_congruence_holds,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_congruence_data,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_pair_row_from_congruence_data,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_primitive_factor_determinant_residue_rows,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(parallel_direction_factor_witness_data, m)?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_witness_row_data,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(ray_parallel_factor_residues, m)?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_residue_classes,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_integrality_strip_intersection_residue_count,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        pythagorean_lattice_pair_strip_linear_congruence,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(two_variable_linear_congruence_gcd, m)?)?;
    m.add_function(wrap_pyfunction!(
        two_variable_linear_congruence_pair_data,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        pythagorean_lattice_pair_strip_crt_data,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        pythagorean_lattice_pair_same_strip_combined_linear_congruence,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        pythagorean_lattice_pair_same_strip_intersection_residue_count,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(pythagorean_lattice_pair_witness, m)?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_certificate_midpoint,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(parallel_direction_cover_midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(register_lattice_pairs, m)?)?;
    m.add_function(wrap_pyfunction!(first_registered_lattice_midpoint, m)?)?;
    Ok(())
}
