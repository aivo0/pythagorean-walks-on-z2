use pyo3::exceptions::PyValueError;
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

fn lattice_coefficients(
    target: (i64, i64),
    first_direction: (i64, i64),
    second_direction: (i64, i64),
) -> Option<(i64, i64)> {
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
        (first_numerator / determinant_value) as i64,
        (second_numerator / determinant_value) as i64,
    ))
}

fn lattice_pair_witness_from_pairs(
    target: (i64, i64),
    pairs: &[LatticePair],
) -> Option<((i64, i64), (i64, i64), i64, i64, i64)> {
    for pair in pairs {
        let Some((first_coefficient, second_coefficient)) =
            lattice_coefficients(target, pair.first, pair.second)
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

fn registered_lattice_pairs() -> &'static Mutex<HashMap<String, Vec<LatticePair>>> {
    LATTICE_PAIR_REGISTRY.get_or_init(|| Mutex::new(HashMap::new()))
}

fn parallel_direction_factor_midpoint(
    target: (i64, i64),
    direction: (i64, i64),
    factor: i64,
) -> Option<(i64, i64)> {
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
    if first_coefficient == 0 {
        return None;
    }
    let midpoint = (
        (first_coefficient * u) as i64,
        (first_coefficient * v) as i64,
    );
    if certificate_valid(target, midpoint) {
        Some(midpoint)
    } else {
        None
    }
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

#[pyfunction]
fn edge_delta(dx: i64, dy: i64) -> bool {
    if dx == 0 || dy == 0 {
        return false;
    }
    let dx = dx as i128;
    let dy = dy as i128;
    is_square_i128(dx * dx + dy * dy)
}

#[pyfunction]
fn certificate_valid(target: (i64, i64), midpoint: (i64, i64)) -> bool {
    let (gx, gy) = target;
    let (x, y) = midpoint;
    edge_delta(x, y) && edge_delta(gx - x, gy - y)
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
    m.add_function(wrap_pyfunction!(prime_power_factorization, m)?)?;
    m.add_function(wrap_pyfunction!(prime_factors, m)?)?;
    m.add_function(wrap_pyfunction!(positive_divisors, m)?)?;
    m.add_function(wrap_pyfunction!(divisor_residue_classes, m)?)?;
    m.add_function(wrap_pyfunction!(has_divisor_in_residue_classes, m)?)?;
    m.add_function(wrap_pyfunction!(parallel_direction_factor_modulus, m)?)?;
    m.add_function(wrap_pyfunction!(ray_parallel_factor_residues, m)?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_residue_classes,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        parallel_direction_factor_integrality_strip_intersection_residue_count,
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
