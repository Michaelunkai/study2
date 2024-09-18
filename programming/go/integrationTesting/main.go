package main

import (
    "database/sql"
    "fmt"
    "net/http"

    _ "github.com/mattn/go-sqlite3"
)

func helloHandler(db *sql.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var greeting string
        err := db.QueryRow("SELECT greeting FROM greetings WHERE id = 1").Scan(&greeting)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
        fmt.Fprintf(w, greeting)
    }
}

func main() {
    db, err := sql.Open("sqlite3", "./test.db")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    http.HandleFunc("/hello", helloHandler(db))
    http.ListenAndServe(":8080", nil)
}
