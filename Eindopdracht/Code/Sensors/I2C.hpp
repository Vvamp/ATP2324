#ifndef I2C_HPP
#define I2C_HPP

#include <vector>
using std::vector;

class I2C_Device{
public:
    I2C_Device(uint8_t i2c_address) : address(i2c_address){};


private:
    uint8_t address;
}

class I2C_Bus{
public:
    void register_device(I2C_Device device){
        registered_devices.push_back(device);
    }



private:
    vector<I2C_Device> registered_devices;
    

};

class I2C{
public:
    I2C(uint8_t i2c_address, int SCL, int SDA) : SCL(SCL), SDA(SDA) {}
    uint8_t read(){
        
    }
    void write(uint8_t data);
private:
    int  SCL;
    int  SDA
};

#endif //I2C_HPP