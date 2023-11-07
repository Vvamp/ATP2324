#ifndef ISENSOR_HPP
#define ISENSOR_HPP
#include <pybind11/pybind11.h>

namespace py = pybind11;

class ISensor{
public:
    virtual float read() = 0;
    virtual py::object readSimulated(py::object plant) = 0;
};

#endif // ISENSOR_HPP