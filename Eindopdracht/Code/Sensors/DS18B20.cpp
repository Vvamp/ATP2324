#include "DS18B20.hpp"

float DS18B20::getTempC(){
    return 15;
}

float DS18B20::read(){
    return getTempC();
}

py::object DS18B20::readSimulated(py::object plant){
    py::object aquarium = plant.attr("aquarium");
    py::object water_temp = aquarium.attr("water_temperature");
    return water_temp;
}

PYBIND11_MODULE(DS18B20, m)
{
    py::class_<ISensor>(m, "ISensor").def("read", &ISensor::read).def("readSimulated", &ISensor::readSimulated);
    py::class_<IThermometer>(m, "IThermometer").def("getTempC", &IThermometer::getTempC);
    py::class_<DS18B20, IThermometer>(m, "DS18B20").def("getTempC", &DS18B20::getTempC).def("read", &DS18B20::read).def("readSimulated", &DS18B20::readSimulated).def(py::init<uint8_t>());
}