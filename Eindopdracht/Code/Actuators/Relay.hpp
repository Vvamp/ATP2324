#ifndef RELAY_HPP
#define RELAY_HPP

#include <iostream>
#include <pybind11/pybind11.h>
#include "IRelay.hpp"

namespace py = pybind11;

class Relay : public IRelay
{
public:
    Relay(int pinNumber) : pinNumber(pinNumber), pinState(false){};

    void turnOn();
    void turnOff();
    bool getState();

private:
    int pinNumber;
    bool pinState;
};

#endif // relay.hpp