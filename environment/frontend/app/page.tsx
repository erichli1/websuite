"use client";

import { Link, Stack, Typography } from "@mui/material";
import { ALL_TESTS } from "./utils";

export default function Home() {
  const tasksTests: [string, string][] = [];

  Object.keys(ALL_TESTS).forEach((outerKey) => {
    Object.keys(ALL_TESTS[outerKey]).forEach((innerKey) => {
      tasksTests.push([outerKey, innerKey]);
    });
  });

  return (
    <main>
      <Stack
        maxWidth="sm"
        sx={{ marginX: "auto", padding: "1rem" }}
        spacing={2}
      >
        <Typography variant="h2" textAlign="center">
          web agent benchmark
        </Typography>
        <Typography>
          To see individual tests, please navigate to /ind/(task)?test=(test)
        </Typography>

        {tasksTests.map(([task, test]) => (
          <Link
            key={`${task}/${test}`}
            href={`/ind/${task}?test=${test}`}
          >{`${task}/${test}`}</Link>
        ))}
      </Stack>
    </main>
  );
}
