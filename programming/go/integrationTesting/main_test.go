package main

import (
    "database/sql"
    "net/http"
    "net/http/httptest"
    "testing"

    _ "github.com/mattn/go-sqlite3"
)

func setupTestDB() (*sql.DB, error) {
    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        return nil, err
    }

    createTable := `CREATE TABLE greetings (id INTEGER PRIMARY KEY, greeting TEXT);`
    _, err = db.Exec(createTable)
    if err != nil {
        return nil, err
    }

    insertData := `INSERT INTO greetings (id, greeting) VALUES (1, 'Hello, World!');`
    _, err = db.Exec(insertData)
    if err != nil {
        return nil, err
    }

    return db, nil
}

func TestHelloHandler(t *testing.T) {
    db, err := setupTestDB()
    if err != nil {
        t.Fatalf("Failed to set up test DB: %v", err)
    }
    defer db.Close()

    req, err := http.NewRequest("GET", "/hello", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(helloHandler(db))
    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }

    expected := "Hello, World!"
    if rr.Body.String() != expected {
        t.Errorf("handler returned unexpected body: got %v want %v", rr.Body.String(), expected)
    }
}
