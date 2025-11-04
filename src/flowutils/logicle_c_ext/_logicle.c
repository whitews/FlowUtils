#include <Python.h>
#include <numpy/arrayobject.h>
#include "logicle.h"

static PyObject *wrap_logicle_scale(PyObject *self, PyObject *args) {
    double t, w, m, a;
    PyObject *x;

    // parse the input args tuple
    if (!PyArg_ParseTuple(args, "ddddO", &t, &w, &m, &a, &x)) {
        return NULL;
    }

    PyArrayObject *x_array = (PyArrayObject *) PyArray_FROM_OTF(x, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    // throw exception if the array doesn't exist
    if (!x_array) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert x to NumPy array");
        return NULL;
    }

    // get length of input array
    int n = (int)PyArray_DIM(x_array, 0);

    // get pointers to the data as C-type
    double *xc = (double*)PyArray_DATA(x_array);

    // now we can call our function!
    logicle_scale(t, w, m, a, xc, n);

    return (PyObject *) x_array;
}

static PyObject *wrap_logicle_inverse(PyObject *self, PyObject *args) {
    double t, w, m, a;
    PyObject *x;

    // parse the input args tuple
    if (!PyArg_ParseTuple(args, "ddddO", &t, &w, &m, &a, &x)) {
        return NULL;
    }

    // read the numpy array
    PyArrayObject *x_array = (PyArrayObject *) PyArray_FROM_OTF(x, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (!x_array) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert x to NumPy array");
        return NULL;
    }

    // get length of input array
    int n = (int)PyArray_DIM(x_array, 0);

    // get pointers to the data as C-type
    double *xc = (double*)PyArray_DATA(x_array);

    // now we can call our function!
    logicle_inverse(t, w, m, a, xc, n);

    return (PyObject *) x_array;
}

static PyObject *wrap_hyperlog_scale(PyObject *self, PyObject *args) {
    double t, w, m, a;
    PyObject *x;

    // parse the input args tuple
    if (!PyArg_ParseTuple(args, "ddddO", &t, &w, &m, &a, &x)) {
        return NULL;
    }

    // read the numpy array
    PyArrayObject *x_array = (PyArrayObject *) PyArray_FROM_OTF(x, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (!x_array) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert x to NumPy array");
        return NULL;
    }

    // get length of input array
    int n = (int)PyArray_DIM(x_array, 0);

    // get pointers to the data as C-type
    double *xc = (double*)PyArray_DATA(x_array);

    // now we can call our function!
    hyperlog_scale(t, w, m, a, xc, n);

    return (PyObject *) x_array;
}

static PyObject *wrap_hyperlog_inverse(PyObject *self, PyObject *args) {
    double t, w, m, a;
    PyObject *x;

    // parse the input args tuple
    if (!PyArg_ParseTuple(args, "ddddO", &t, &w, &m, &a, &x)) {
        return NULL;
    }

    // read the numpy array
    PyArrayObject *x_array = (PyArrayObject *) PyArray_FROM_OTF(x, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (!x_array) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to convert x to NumPy array");
        return NULL;
    }

    // get length of input array
    int n = (int)PyArray_DIM(x_array, 0);

    // get pointers to the data as C-type
    double *xc = (double*)PyArray_DATA(x_array);

    // now we can call our function!
    hyperlog_inverse(t, w, m, a, xc, n);

    return (PyObject *) x_array;
}


static PyMethodDef module_methods[] = {
    {"logicle_scale", wrap_logicle_scale, METH_VARARGS, NULL},
    {"logicle_inverse", wrap_logicle_inverse, METH_VARARGS, NULL},
    {"hyperlog_scale", wrap_hyperlog_scale, METH_VARARGS, NULL},
    {"hyperlog_inverse", wrap_hyperlog_inverse, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef logicledef = {
    PyModuleDef_HEAD_INIT,
    "logicle_c",
    NULL,
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit_logicle_c(void) {
    PyObject *m = PyModule_Create(&logicledef);
    if (m == NULL) {
        return NULL;
    }

    import_array(); 
    if (PyErr_Occurred()) {  
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
#else
PyMODINIT_FUNC initlogicle_c(void) {
    PyObject *m = Py_InitModule3("logicle_c", module_methods, NULL);
    if (m == NULL) {
        return;
    }

    import_array();  
    if (PyErr_Occurred()) {
        Py_DECREF(m);
        return;
    }

    return;
}
#endif

