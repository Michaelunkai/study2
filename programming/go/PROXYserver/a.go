package main

import (
    "io"
    "log"
    "net/http"
    "net/url"
)

func handleProxy(w http.ResponseWriter, r *http.Request) {
    targetURL, err := url.Parse(r.RequestURI)
    if err != nil {
        log.Printf("Invalid URL: %v", err)
        http.Error(w, "Invalid URL", http.StatusBadRequest)
        return
    }

    proxyReq, err := http.NewRequest(r.Method, targetURL.String(), r.Body)
    if err != nil {
        log.Printf("Could not create request: %v", err)
        http.Error(w, "Could not create request", http.StatusInternalServerError)
        return
    }

    proxyReq.Header = r.Header

    client := &http.Client{}
    resp, err := client.Do(proxyReq)
    if err != nil {
        log.Printf("Could not reach the server: %v", err)
        http.Error(w, "Could not reach the server", http.StatusBadGateway)
        return
    }
    defer resp.Body.Close()

    log.Printf("Proxying response: %s", resp.Status)

    for k, v := range resp.Header {
        for _, value := range v {
            w.Header().Add(k, value)
        }
    }
    w.WriteHeader(resp.StatusCode)
    io.Copy(w, resp.Body)
}

func main() {
    http.HandleFunc("/", handleProxy)
    log.Println("Starting proxy server on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
