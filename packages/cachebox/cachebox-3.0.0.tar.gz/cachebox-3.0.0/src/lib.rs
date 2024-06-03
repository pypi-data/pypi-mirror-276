use pyo3::prelude::*;

mod basic;
mod cache;
mod fifocache;
mod lfucache;
mod lrucache;
mod rrcache;
mod ttlcache;
mod vttlcache;

#[pymodule]
#[pyo3(name = "_cachebox")]
fn _cachebox(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add("__author__", "awolverp")?;

    m.add_class::<crate::basic::BaseCacheImpl>()?;
    m.add_class::<crate::cache::Cache>()?;
    m.add_class::<crate::fifocache::FIFOCache>()?;
    m.add_class::<crate::lfucache::LFUCache>()?;
    m.add_class::<crate::rrcache::RRCache>()?;
    m.add_class::<crate::lrucache::LRUCache>()?;
    m.add_class::<crate::ttlcache::TTLCache>()?;
    m.add_class::<crate::vttlcache::VTTLCache>()?;

    // iterators
    m.add_class::<crate::basic::iter::tuple_ptr_iterator>()?;
    m.add_class::<crate::basic::iter::object_ptr_iterator>()?;
    m.add_class::<crate::lfucache::lfu_tuple_ptr_iterator>()?;
    m.add_class::<crate::lfucache::lfu_object_ptr_iterator>()?;
    m.add_class::<crate::ttlcache::ttl_tuple_ptr_iterator>()?;
    m.add_class::<crate::ttlcache::ttl_object_ptr_iterator>()?;
    m.add_class::<crate::vttlcache::vttl_tuple_ptr_iterator>()?;
    m.add_class::<crate::vttlcache::vttl_object_ptr_iterator>()?;

    Ok(())
}
