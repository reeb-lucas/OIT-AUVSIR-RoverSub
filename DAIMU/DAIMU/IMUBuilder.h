#pragma once
#include <string>
#include <cstdint>

using namespace std;

class IMUBuilder
{
	public:
		struct internalMeasurementUnit 
		{
			string name;
			int id;
			uint8_t data[];
		};
	private:
		internalMeasurementUnit getIMU(string name);
		void setIMU(string name, int id, uint8_t data[]);
		string getIMUData(string name);
		void setIMUData(string name, uint8_t data[]);
		void storeData(internalMeasurementUnit IMU);
		int verifyData(uint8_t data[]);
};

