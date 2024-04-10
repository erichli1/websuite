"use client";

export default function Home() {
  return (
    <main>
      <h1>basic website</h1>
      <button
        onClick={() =>
          fetch("/log/individual", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ log: "Clicked 'log this!'" }),
          })
        }
      >
        log this!
      </button>
    </main>
  );
}
