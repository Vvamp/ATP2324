#ifndef MCP9808_HPP
#define MCP9808_HPP

#include <pybind11/pybind11.h>
#include "IThermometer.hpp"
#include "ISensor.hpp"
namespace py = pybind11;

class MCP9808 : public IThermometer, public ISensor{
public:
    MCP9808(uint8_t pin_scl, uint8_t pin_sda) : SCL(pin_scl), SDA(pin_sda)
    {}

    float getTempC();
    float read() override;
    py::object readSimulated(py::object plant) override;


private:
    uint8_t SCL;
    uint8_t SDA;
    uint8_t address = 0b0011111; // last 3 bits are set externally
};

#endif // MCP9808_HPP