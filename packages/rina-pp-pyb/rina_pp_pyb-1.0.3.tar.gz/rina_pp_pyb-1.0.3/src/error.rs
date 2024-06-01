use pyo3::{create_exception, exceptions::PyException};

create_exception!(rina_pp_pyb, ArgsError, PyException);
create_exception!(rina_pp_pyb, ParseError, PyException);
create_exception!(rina_pp_pyb, ConvertError, PyException);
