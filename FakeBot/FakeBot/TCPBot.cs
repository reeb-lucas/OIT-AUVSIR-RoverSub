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
        private struct IMU
        {
            public string name;
            public int id;
            public byte[] ? data;
        }
        private IMU frontalGyroAccMag;
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

        static byte[] AccessIMUs(string accessType, bool displayConnected)
        {
            List<IMU> IMUs = new List<IMU>();
            //WitMotion WT901C TTL 9 Axis IMU Sensor Tilt Angle Roll Pitch Yaw + Acceleration + Gyroscope + Magnetometer MPU9250 on PC/Android/MCU
            IMU frontalGyroAccMag = new IMU
            {
                name = "WitMotion-WT901C",
                id = 0,
                data = Encoding.ASCII.GetBytes("")
            };
            string rString;
            if (displayConnected)
                rString = "T ";
            else
                rString = "F ";
            //format of response: Name::ID
            //This is initial access, just getting names and IDs of IMUs
            if (accessType == "Init")
                foreach(IMU imu in IMUs)
                {
                    rString += imu.name + "::" + imu.id + " ";//Yes it is space terminated right now. If you are reading this and want to add the line to get rid of the last space go for it.
                }
            //format of response: Name::ID::Data
            //This is for getting data from the IMUs. Since this is a fake bot it will randomly choose movement patterns here
            else if (accessType == "Get")
            {
                //TODO: this
                throw new NotImplementedException();
            }

            byte[] response = Encoding.ASCII.GetBytes(rString);
            return response;
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
            bool displayConnected = DisplayConnected(true);
            string requestString = Encoding.ASCII.GetString(request, 0, bytesRead);

            Console.WriteLine(requestString);
            //TODO: This is where FakeBot sends fake IMU data to the program
            byte[] response = new byte[4096];
            if (requestString == "iRequest")
                response = InitializationRequestHandler(stream, displayConnected);
            else if (requestString == "gRequest")
                response = GetRequestHandler(stream, displayConnected);
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
        private static byte[] InitializationRequestHandler(NetworkStream stream, bool displayConnected)
        {
            //for each IMU, send IMU Name and IMU ID
            byte[] response = new byte[4096];
            response = AccessIMUs("Init", displayConnected);
            return response;
        }

        /// <summary>
        /// Intended to be used by all noninitial requests. Key assumption: IMUs
        /// will always be accessed in the same order
        /// Output:
        /// IMU ID - Based off of port IMU is connected to, begins at 0
        /// All IMU datapoints (varies by IMU type)
        /// </summary>
        /// <param name="stream"></param>
        private static byte[] GetRequestHandler(NetworkStream stream, bool displayConnected)
        {
            //Get IMUs and their data
            byte[] response = new byte[4096];
            response = AccessIMUs("Get", displayConnected);
            return response;
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