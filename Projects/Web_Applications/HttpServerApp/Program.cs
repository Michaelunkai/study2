using System;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ProfessionalHttpServerApp
{
    class Program
    {
        static async Task Main(string[] args)
        {
            HttpListener listener = new HttpListener();
            listener.Prefixes.Add("http://localhost:5000/");
            listener.Start();
            Console.WriteLine("HTTP Server is running. Listening on http://localhost:5000/");

            // Register a handler to catch SIGINT (Ctrl+C) for graceful shutdown
            var cts = new CancellationTokenSource();
            Console.CancelKeyPress += (sender, eventArgs) => {
                eventArgs.Cancel = true;
                cts.Cancel();
            };

            try
            {
                while (!cts.Token.IsCancellationRequested)
                {
                    var context = await listener.GetContextAsync();
                    _ = Task.Run(() => HandleRequest(context));
                }
            }
            catch (HttpListenerException) when (cts.Token.IsCancellationRequested)
            {
                // Listener stopped
            }
            finally
            {
                listener.Close();
                Console.WriteLine("HTTP Server has stopped.");
            }
        }

        static async Task HandleRequest(HttpListenerContext context)
        {
            var request = context.Request;
            var response = context.Response;

            Logger.LogRequest(request);

            string filePath = $"wwwroot{request.Url.AbsolutePath}";
            if (request.Url.AbsolutePath == "/")
            {
                filePath = "wwwroot/index.html";
            }

            await ServeStaticFile(response, filePath);

            Logger.LogResponse(response);
        }

        static async Task ServeStaticFile(HttpListenerResponse response, string filePath)
        {
            if (File.Exists(filePath))
            {
                byte[] buffer = await File.ReadAllBytesAsync(filePath);
                response.ContentType = GetContentType(filePath);
                response.ContentLength64 = buffer.Length;
                await response.OutputStream.WriteAsync(buffer, 0, buffer.Length);
                response.OutputStream.Close();
            }
            else
            {
                response.StatusCode = (int)HttpStatusCode.NotFound;
                response.Close();
            }
        }

        static string GetContentType(string filePath)
        {
            string extension = Path.GetExtension(filePath).ToLowerInvariant();
            return extension switch
            {
                ".html" => "text/html",
                ".css" => "text/css",
                ".js" => "application/javascript",
                _ => "application/octet-stream",
            };
        }
    }

    static class Logger
    {
        public static void LogRequest(HttpListenerRequest request)
        {
            Console.WriteLine($"{DateTime.Now}: {request.HttpMethod} {request.Url}");
        }

        public static void LogResponse(HttpListenerResponse response)
        {
            Console.WriteLine($"{DateTime.Now}: Response {response.StatusCode}");
        }
    }
}
