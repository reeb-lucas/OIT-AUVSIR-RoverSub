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
        private readonly string[] IMUstring = { "a" }; //https://www.dotnetperls.com/keyvaluepair
        private readonly List<string> IMUs = new List<string>(IMUstring);
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

        /// <summary>
        /// Handles the requests from the Senior Project Program by redirecting 
        /// to other functions
        /// </summary>
        /// <param name="tcpClient"></param>
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
            byte[] response = new byte[4096];
            if (requestString == "iRequest")
                response = InitializationRequestHandler(stream);
            else if (requestString == "gRequest")
                response = GetRequestHandler(stream);
            else if (requestString == null)
                response = Encoding.ASCII.GetBytes("Failed to complete request. Null requestString.");
            else
                response = Encoding.ASCII.GetBytes("Failed to complete request. Unexpected requestString.");

            stream.Write(response, 0, response.Length);
            tcpClient.Close();//Note will loop when TODO is done so it does not close after one response
        }

        /// <summary>
        /// Intended to be used for the first request. Key assumption: IMUs will 
        /// always be accessed in the same order
        /// Output:
        /// IMU Name - Type of unit
        /// IMU ID - Based off of port IMU is connected to, begins at 0
        /// </summary>
        /// <param name="stream"></param>
        private static byte[] InitializationRequestHandler(NetworkStream stream)
        {
            //for each IMU, send IMU Name and IMU ID
            throw new NotImplementedException();
        }

        /// <summary>
        /// Intended to be used by all noninitial requests. Key assumption: IMUs
        /// will always be accessed in the same order
        /// Output:
        /// IMU ID - Based off of port IMU is connected to, begins at 0
        /// All IMU datapoints (varies by IMU type)
        /// </summary>
        /// <param name="stream"></param>
        private static byte[] GetRequestHandler(NetworkStream stream)
        {
            throw new NotImplementedException();
        }

        /// <summary>
        /// Returns if a display is connected or not. This is hardcoded as this is a emulation of the bot.
        /// Output:
        /// T/F based logically on if a display is connected
        /// </summary>
        /// <param name="displayConnected"></param>
        private static bool DisplayConnected(bool displayConnected)
        {
            if(displayConnected)
                return true;
            else
                return false;
        }
    }
}