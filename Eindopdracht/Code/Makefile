CXX = g++
CXXFLAGS = -O3 -Wall -shared -std=c++11 -fPIC
PYBIND11_INCLUDES = $(shell python -m pybind11 --includes)
PYTHON_EXT_SUFFIX = $(shell python-config --extension-suffix)
SRC_DIR = ./
SENSOR_DIR = $(SRC_DIR)/Sensors
ACTUATOR_DIR = $(SRC_DIR)/Actuators

# Automatically list all C++ files in the sensor and actuator directories
SENSOR_SOURCES = $(wildcard $(SENSOR_DIR)/*.cpp)
ACTUATOR_SOURCES = $(wildcard $(ACTUATOR_DIR)/*.cpp)
SENSOR_TARGETS = $(SENSOR_SOURCES:$(SENSOR_DIR)/%.cpp=$(SENSOR_DIR)/%$(PYTHON_EXT_SUFFIX))
ACTUATOR_TARGETS = $(ACTUATOR_SOURCES:$(ACTUATOR_DIR)/%.cpp=$(ACTUATOR_DIR)/%$(PYTHON_EXT_SUFFIX))

all: sensors actuators

sensors: $(SENSOR_TARGETS)

actuators: $(ACTUATOR_TARGETS)

$(SENSOR_DIR)/%$(PYTHON_EXT_SUFFIX): $(SENSOR_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(PYBIND11_INCLUDES) $< -o $@

$(ACTUATOR_DIR)/%$(PYTHON_EXT_SUFFIX): $(ACTUATOR_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(PYBIND11_INCLUDES) $< -o $@

clean:
	rm -f $(SENSOR_DIR)/*$(PYTHON_EXT_SUFFIX) $(ACTUATOR_DIR)/*$(PYTHON_EXT_SUFFIX)


run: all
	python main.py