#include "IMUBuilder.h"

IMUBuilder::internalMeasurementUnit IMUBuilder::getIMU(string name)
{
	return internalMeasurementUnit();
}

void IMUBuilder::setIMU(string name, int id, uint8_t data[])
{
}

string IMUBuilder::getIMUData(string name)
{
	return string();
}

void IMUBuilder::setIMUData(string name, uint8_t data[])
{
}

void IMUBuilder::storeData(internalMeasurementUnit IMU)
{
}

int IMUBuilder::verifyData(uint8_t data[])
{
	return 0;
}