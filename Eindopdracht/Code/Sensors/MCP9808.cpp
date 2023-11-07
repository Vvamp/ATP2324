#include "MCP9808.hpp"

float MCP9808::getTempC(){
    return 15;
}

float MCP9808::read(){
    return getTempC();
}

py::object MCP9808::readSimulated(py::object plant){
    py::object room_temp = plant.attr("room_temperature");
    return room_temp;
}

PYBIND11_MODULE(MCP9808, m)
{
    py::class_<MCP9808, IThermometer>(m, "MCP9808").def("getTempC", &MCP9808::getTempC).def("read", &MCP9808::read).def("readSimulated", &MCP9808::readSimulated).def(py::init<uint8_t, uint8_t>());
}