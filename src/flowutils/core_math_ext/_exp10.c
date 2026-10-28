#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

// External CORE-MATH function
extern double cr_exp10(double x);

static PyObject* py_cr_exp10(PyObject *self, PyObject *args) {
    PyObject *input_obj;
    if (!PyArg_ParseTuple(args, "O", &input_obj)) {
        return NULL;
    }

    // Handle scalar float/int case
    if (PyFloat_Check(input_obj) || PyLong_Check(input_obj)) {
        double val = PyFloat_AsDouble(input_obj);
        if (PyErr_Occurred()) return NULL;
        return PyFloat_FromDouble(cr_exp10(val));
    }

    // If it's a NumPy array, use NumPy C-API directly for robust layout handling
    if (PyArray_Check(input_obj)) {
        // Enforce that the array is C-contiguous and behavior behaves as NPY_DOUBLE
        PyArrayObject *np_in = (PyArrayObject*)PyArray_FROM_OTF(input_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
        if (!np_in) return NULL; // PyArray_FROM_OTF sets the TypeError/ValueError prior

        int ndim = PyArray_NDIM(np_in);
        npy_intp *dims = PyArray_DIMS(np_in);
        Py_ssize_t n = PyArray_SIZE(np_in);

        // First, create output array with identical dimensions
        PyObject *out_array = PyArray_SimpleNew(ndim, dims, NPY_DOUBLE);
        if (!out_array) {
            Py_DECREF(np_in);
            return NULL;
        }

        const double *in_ptr = (const double*)PyArray_DATA(np_in);
        double *out_ptr = (double*)PyArray_DATA((PyArrayObject*)out_array);

        for (Py_ssize_t i = 0; i < n; i++) {
            out_ptr[i] = cr_exp10(in_ptr[i]);
        }

        Py_DECREF(np_in);
        return out_array;
    }

    // Fallback for non-NumPy buffers (e.g. standard Python array.array or bytes)
    Py_buffer view;
    if (PyObject_GetBuffer(input_obj, &view, PyBUF_SIMPLE) != 0) {
        PyErr_SetString(PyExc_TypeError, "Input must be a scalar or a numeric array.");
        return NULL;
    }

    if (view.itemsize != sizeof(double)) {
        PyBuffer_Release(&view);
        PyErr_SetString(PyExc_ValueError, "Array must be of float64 type.");
        return NULL;
    }

    Py_ssize_t n = view.len / sizeof(double);
    const double *in_ptr = (const double*)view.buf;

    npy_intp dims[1] = {n};
    PyObject *out_array = PyArray_SimpleNew(1, dims, NPY_DOUBLE);
    if (!out_array) {
        PyBuffer_Release(&view);
        return NULL;
    }

    double *out_ptr = (double*)PyArray_DATA((PyArrayObject*)out_array);

    for (Py_ssize_t i = 0; i < n; i++) {
        out_ptr[i] = cr_exp10(in_ptr[i]);
    }

    PyBuffer_Release(&view);
    return out_array;
}

static PyMethodDef ModuleMethods[] = {
    {"exp10_c", py_cr_exp10, METH_VARARGS, "Correctly rounded 10^x exponential function."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "exp10_c",
    "CORE-MATH cr_exp10 C extension",
    -1,
    ModuleMethods
};

// Init function to safely handle NumPy macro expansions
PyObject* PyInit_real_exp10_c(void) {
    import_array();
    if (PyErr_Occurred()) return NULL;
    return PyModule_Create(&moduledef);
}

PyMODINIT_FUNC PyInit_exp10_c(void) {
    return PyInit_real_exp10_c();
}