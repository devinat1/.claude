package main

import (
	"fmt"
	"net/http"
	"os"
	"time"
)

// Simulated DB connection pool. A buffered channel models a fixed number of
// connections; receiving from it = checking out a connection, sending back =
// releasing it. Each query holds a connection for queryDuration. There is no
// real database — the pool size IS the bottleneck, which is the whole lesson.

const queryDuration = 40 * time.Millisecond

func main() {
	mode := os.Getenv("MODE")
	if mode == "" {
		mode = "naive"
	}

	var poolSize int
	var acquireTimeout time.Duration
	switch mode {
	case "naive":
		poolSize = 5       // under-provisioned: exhausts under load
		acquireTimeout = 0 // no timeout: requests queue unboundedly
	case "patched":
		poolSize = 100                          // right-sized for the offered concurrency
		acquireTimeout = 250 * time.Millisecond // fail fast instead of melting down
	default:
		fmt.Println("MODE must be naive or patched")
		os.Exit(1)
	}

	pool := make(chan struct{}, poolSize)
	for i := 0; i < poolSize; i++ {
		pool <- struct{}{}
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if acquireTimeout == 0 {
			<-pool // block until a connection frees up, however long that takes
		} else {
			select {
			case <-pool:
			case <-time.After(acquireTimeout):
				http.Error(w, "pool exhausted", http.StatusServiceUnavailable)
				return
			}
		}
		defer func() { pool <- struct{}{} }()

		time.Sleep(queryDuration) // the "query"
		fmt.Fprintln(w, "ok")
	})

	fmt.Printf("listening on :8081 mode=%s pool=%d\n", mode, poolSize)
	http.ListenAndServe(":8081", nil)
}
