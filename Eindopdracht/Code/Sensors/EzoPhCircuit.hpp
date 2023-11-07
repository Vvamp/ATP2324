#ifndef EzoPhCircuit_HPP
#define EzoPhCircuit_HPP

#include <pybind11/pybind11.h>
#include "IpHSensor.hpp"
#include "ISensor.hpp"

namespace py = pybind11;

class EzoPhCircuit : public IpHSensor, public ISensor{
public:
    EzoPhCircuit(uint8_t pin_scl, uint8_t pin_sda) : SCL(pin_scl), SDA(pin_sda)
    {}

    float getPh();
    float read() override;
    py::object readSimulated(py::object plant) override;

private:
    uint8_t SCL;
    uint8_t SDA;
    uint8_t address = 0x63;
};

#endif // EzoPhCircuit_HPP