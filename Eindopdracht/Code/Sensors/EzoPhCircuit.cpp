#include "EzoPhCircuit.hpp"

float EzoPhCircuit::getPh(){
    return 5.001;
}

float EzoPhCircuit::read(){
    return getPh();
}

py::object EzoPhCircuit::readSimulated(py::object plant){
    py::object aquarium = plant.attr("aquarium");
    py::object ph = aquarium.attr("ph");
    return ph;
}

PYBIND11_MODULE(EzoPhCircuit, m)
{
    py::class_<IpHSensor>(m, "IpHSensor").def("getPh", &IpHSensor::getPh);
    py::class_<EzoPhCircuit, IpHSensor>(m, "EzoPhCircuit").def("getPh", &EzoPhCircuit::getPh).def("read", &EzoPhCircuit::read).def("readSimulated", &EzoPhCircuit::readSimulated).def(py::init<uint8_t, uint8_t>());
}