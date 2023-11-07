#include "relay.hpp"

void Relay::turnOn()
{
    std::cout << "> Turning on relay\n";
    pinState = true;
}

void Relay::turnOff()
{
    std::cout << "> Turning off relay\n";
    pinState = false;
}

bool Relay::getState() { return pinState; }

PYBIND11_MODULE(relay, m)
{
    py::class_<Relay>(m, "Relay").def("turnOn", &Relay::turnOn).def("turnOff", &Relay::turnOff).def("getState", &Relay::getState).def(py::init<int>());
}

// PYBIND11_MODULE(relay, m)
// {
//     py::class_<IActuator>(m, "IActuator").def("turnOn", &IActuator::turnOn).def("turnOff", &IActuator::turnOff);
// }
