#ifndef DS18B20_HPP
#define DS18B20_HPP

#include <pybind11/pybind11.h>
#include "IThermometer.hpp"
#include "ISensor.hpp"

namespace py = pybind11;

class DS18B20 : public IThermometer, public ISensor {
public:
    DS18B20(uint8_t one_wire_pin) : pin_number(one_wire_pin)
    {}

    float getTempC();
    float read() override;
    py::object readSimulated(py::object plant) override;

private:
    int pin_number;
};

#endif // DS18B20_HPP