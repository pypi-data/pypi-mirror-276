// Copyright 2018 Ivan Porto Carrero
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

use std::fmt::{self, Display};
use std::ops::Deref;
use std::str;
use std::sync::Mutex;

use rand::distributions::Alphanumeric;
use rand::rngs::OsRng;
use rand::thread_rng;
use rand::Rng;
use pyo3::prelude::{pymethods, pyclass, pyfunction, pymodule, PyResult, Python, PyModule};

const BASE: usize = 62;
const ALPHABET: [u8; BASE] = *b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

const PRE_LEN: usize = 12;
const MAX_SEQ: u64 = 839_299_365_868_340_224; // (BASE ^ remaining bytes 22 - 12) == 62^10
const MIN_INC: u64 = 33;
const MAX_INC: u64 = 333;

/// The number of bytes/characters of a NUID.
pub const TOTAL_LEN: usize = 22;

static GLOBAL_NUID: Mutex<NUID> = Mutex::new(NUID::new());

/// Generate the next `NUID` string from the global locked `NUID` instance.
#[allow(clippy::missing_panics_doc)]
#[must_use]
#[pyfunction]
pub fn next() -> NUIDStr {
    GLOBAL_NUID.lock().unwrap().next()
}

/// NUID needs to be very fast to generate and truly unique, all while being entropy pool friendly.
/// We will use 12 bytes of crypto generated data (entropy draining), and 10 bytes of sequential data
/// that is started at a pseudo random number and increments with a pseudo-random increment.
/// Total is 22 bytes of base 62 ascii text :)
#[pyclass]
pub struct NUID {
    pre: [u8; PRE_LEN],
    seq: u64,
    inc: u64,
}

/// An `NUID` string.
///
/// Use [`NUIDStr::as_str`], [`NUIDStr::into_bytes`], the [`Deref`] implementation or
/// [`ToString`] to access the string.
#[pyclass]
pub struct NUIDStr(
    // INVARIANT: this buffer must always contain a valid utf-8 string
    [u8; TOTAL_LEN],
);

impl Default for NUID {
    fn default() -> Self {
        Self::new()
    }
}

#[pymethods]
impl NUID {
    /// generate a new `NUID` and properly initialize the prefix, sequential start, and sequential increment.
    #[must_use]
    #[new]
    pub const fn new() -> Self {
        Self {
            pre: [0; PRE_LEN],
            // the first call to `next` will cause the prefix and sequential to be regenerated
            seq: MAX_SEQ,
            inc: 0,
        }
    }

    pub fn randomize_prefix(&mut self) {
        let rng = OsRng;
        for (i, n) in rng.sample_iter(&Alphanumeric).take(PRE_LEN).enumerate() {
            self.pre[i] = ALPHABET[n as usize % BASE];
        }
    }

    /// Generate the next `NUID` string.
    #[allow(clippy::should_implement_trait)]
    #[must_use]
    pub fn next(&mut self) -> NUIDStr {
        let mut buffer = [0u8; TOTAL_LEN];

        self.seq += self.inc;
        if self.seq >= MAX_SEQ {
            self.randomize_prefix();
            self.reset_sequential();
        }
        #[allow(clippy::cast_possible_truncation)]
            let seq = self.seq as usize;

        for (i, n) in self.pre.iter().enumerate() {
            buffer[i] = *n;
        }

        let mut l = seq;
        for i in (PRE_LEN..TOTAL_LEN).rev() {
            buffer[i] = ALPHABET[l % BASE];
            l /= BASE;
        }

        // `buffer` has been filled with base62 data, which is always valid utf-8
        NUIDStr(buffer)
    }

    fn reset_sequential(&mut self) {
        let mut rng = thread_rng();
        self.seq = rng.gen_range(0..MAX_SEQ);
        self.inc = rng.gen_range(MIN_INC..MAX_INC);
    }
}

#[pymethods]
impl NUIDStr {
    /// Get a reference to the inner string
    #[must_use]
    pub fn as_str(&self) -> &str {
        // SAFETY: the invariant guarantees the buffer to always contain utf-8 characters
        unsafe { str::from_utf8_unchecked(&self.0) }
    }

    /// Extract the inner buffer
    #[must_use]
    pub fn into_bytes(&self) -> [u8; TOTAL_LEN] {
        self.0
    }
}

impl Display for NUIDStr {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

impl Deref for NUIDStr {
    type Target = str;

    /// Get a reference to the inner string
    fn deref(&self) -> &Self::Target {
        self.as_str()
    }
}

#[pymodule]
fn nuid(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<NUID>()?;
    Ok(())
}