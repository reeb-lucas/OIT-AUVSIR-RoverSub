// Tyler Lucas
// Creation Date: 1/5/2022
#include <iostream>
#include <fstream>
#include <sstream>
#include <WinSock2.h>
#include <WS2tcpip.h>

using namespace std;

int main()
{
    //Create TCP connection with FakeBot
    SOCKET sock = INVALID_SOCKET;
    bool connecting = 1;
    while(connecting)
    {
        // Initialize WinSock
        WSADATA wsaData;
        int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
        if (result != 0)
        {
            cerr << "Error initializing WinSock: " << result << endl;
            connecting = 1;
        }

        // Set the IP address and port number for the server
        const char* ipAddress = "127.0.0.1";
        int port = 8888;

        // Create a new socket.
        sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (sock == INVALID_SOCKET)
        {
            cerr << "Error creating socket: " << WSAGetLastError() << endl;
            WSACleanup();
            connecting = 1;
        }

        // Set up sockaddr_in struct
        sockaddr_in serverAddress;
        serverAddress.sin_family = AF_INET;
        serverAddress.sin_port = htons(port);
        inet_pton(AF_INET, ipAddress, &serverAddress.sin_addr);

        // Connect to the server.
        if (connect(sock, (sockaddr*)&serverAddress, sizeof(serverAddress)) == SOCKET_ERROR)
        {
            cerr << "Error connecting to server: " << WSAGetLastError() << endl;
            closesocket(sock);
            WSACleanup();
            connecting = 1;
        }

        connecting = 0;
    }

    //call out to other classes & communicate with server
    

    //close connection to FakeBot
    if(sock != INVALID_SOCKET)
        closesocket(sock);
    WSACleanup();

    return 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
