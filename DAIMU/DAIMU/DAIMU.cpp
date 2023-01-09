// Tyler Lucas
// Creation Date: 1/5/2022
#include <iostream>
#include <fstream>
#include <sstream>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include "IMUBuilder.h"

#define DEFAULT_BUFLEN 512

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
            cerr << "Error initializing WinSock: \n" << result << endl;
            connecting = 1;
        }

        // Set the IP address and port number for the server
        const char* ipAddress = "127.0.0.1";
        int port = 8888;

        // Create a new socket.
        sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (sock == INVALID_SOCKET)
        {
            cerr << "Error creating socket: \n" << WSAGetLastError() << endl;
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
            cerr << "Error connecting to server: \n" << WSAGetLastError() << endl;
            closesocket(sock);
            WSACleanup();
            connecting = 1;
        }

        connecting = 0;
    }

    //call out to other classes & communicate with server
    //below is temp to get proof of communication
    char recvbuf[DEFAULT_BUFLEN];
    int recvbuflen = DEFAULT_BUFLEN;

    const char* tempMsg = "Msg.\n";
    int result;

    if ((send(sock, tempMsg, (int)strlen(tempMsg), 0) == SOCKET_ERROR))
    {
        cerr << "send failed: %d\n" << WSAGetLastError() << endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    //recieve until closes
    do {
        result = recv(sock, recvbuf, recvbuflen, 0);
        if (result > 0)
        {
            printf("Bytes recieved: %d\n", result);
            printf("Message recieved: %s\n", recvbuf);
        }
        else if (result == 0)
            printf("Connection closed\n");
        else
            printf("recv failed: %d\n", WSAGetLastError());

    } while (result > 0);

    //close connection to FakeBot
    if(sock != INVALID_SOCKET)
        closesocket(sock);
    WSACleanup();

    return 0;
}