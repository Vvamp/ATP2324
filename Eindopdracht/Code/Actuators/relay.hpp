#ifndef RELAY_HPP
#define RELAY_HPP

#include <iostream>
#include <pybind11/pybind11.h>
// #include "IActuator.hpp"

namespace py = pybind11;

class Relay
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