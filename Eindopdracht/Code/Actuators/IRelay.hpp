#ifndef IRelay_HPP
#define IRelay_HPP
#include <pybind11/pybind11.h>

namespace py = pybind11;

class IRelay{
public:
    virtual void turnOn() = 0;
    virtual void turnOff() = 0;
};

#endif // IRelay_HPP