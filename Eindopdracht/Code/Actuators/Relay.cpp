#include "Relay.hpp"

void Relay::turnOn()
{
    pinState = true;
}

void Relay::turnOff()
{
    pinState = false;
}

bool Relay::getState() { return pinState; }



PYBIND11_MODULE(Relay, m)
{
    py::class_<IRelay>(m, "IRelay").def("turnOn", &IRelay::turnOn).def("turnOff", &IRelay::turnOff);
    py::class_<Relay, IRelay>(m, "Relay").def("turnOn", &Relay::turnOn).def("turnOff", &Relay::turnOff).def("getState", &Relay::getState).def(py::init<int>());
}

