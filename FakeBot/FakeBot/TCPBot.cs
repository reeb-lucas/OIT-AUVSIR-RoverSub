//Author: Tyler Lucas
//Creation Date: 12/28/2022
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;

namespace FakeBot
{

    /// <summary>
    /// The BotServer class creates a TCP server that will emulate a robot. It will
    /// send data to the connected client (Senior Project program) in place of a 
    /// connection to a real robot with IMUs.
    /// </summary>
    public class BotServer
    {
        static void Main()
        {
            //local
            IPAddress ipa = IPAddress.Parse("127.0.0.1");
            int port = 8888;

            //Listens for a connection on local
            TcpListener listener = new TcpListener(ipa, port);
            listener.Start();

            Console.WriteLine("Listening on port: {0}", port);

            bool done = false;

            while(!done)
            {
                TcpClient tcpClient = listener.AcceptTcpClient();

                //Multiple threads in case needed for testing
                Thread thread = new Thread(() => ClientHandler(tcpClient));
                thread.Start(tcpClient);
            }
        }

        public static void ClientHandler(TcpClient tcpClient)
        {
            IPEndPoint clientIpa = (IPEndPoint)tcpClient.Client.RemoteEndPoint;
            Console.WriteLine("Connected to client at: {0}:{1}", clientIpa.Address, clientIpa.Port);
            NetworkStream stream = tcpClient.GetStream();
            byte[] request = new byte[4096];
            int bytesRead = stream.Read(request, 0, request.Length);
            string requestString = Encoding.ASCII.GetString(request, 0, bytesRead);
            Console.WriteLine(requestString);
            //TODO: This is where FakeBot sends fake IMU data to the program
            byte[] response = Encoding.ASCII.GetBytes("Here is some fake data");
            stream.Write(response, 0, response.Length);
            tcpClient.Close();//Note will loop when TODO is done so it does not close after one response
        }
    }
}