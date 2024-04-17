"use client";

import { ALL_TESTS } from "@/app/utils";
import Typography from "@mui/material/Typography";
import { useSearchParams } from "next/navigation";

export default function Page({ params }: { params: { task: string } }) {
  const searchParams = useSearchParams();
  const task = params.task;
  const test = searchParams.get("test");

  if (test === null) return <Typography>No test provided.</Typography>;
  if (!(task in ALL_TESTS))
    return <Typography>Did not find task: {task}</Typography>;
  if (!(test in ALL_TESTS[task]))
    return (
      <Typography>
        Did not find test: {task}/{test}
      </Typography>
    );

  return ALL_TESTS[task][test];
}
