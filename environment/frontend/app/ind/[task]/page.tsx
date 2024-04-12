"use client";

import { CLICK_TESTS, ClickTestType, TASKS } from "@/app/utils";
import { useSearchParams } from "next/navigation";

export default function Page({ params }: { params: { task: string } }) {
  const searchParams = useSearchParams();
  const test = searchParams.get("test");

  const identifiedTasks = TASKS.filter((task) => task === params.task);
  const identifiedTask = identifiedTasks[0];

  const identifiedTests = CLICK_TESTS.filter((clickTest) => clickTest === test);
  const identifiedTest = identifiedTests[0];

  if (identifiedTasks.length === 0 || identifiedTests.length === 0)
    return <p>Unable to find task or test</p>;

  return (
    <div>
      {identifiedTask === "click" && <ClickTest test={identifiedTest} />}
    </div>
  );
}

function ClickTest({ test }: { test: ClickTestType }) {
  return (
    <>
      {test === "button" && (
        <button
          onClick={() =>
            fetch("/log/individual", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ log: "Clicked button" }),
            })
          }
        >
          Click me
        </button>
      )}
      {test === "link" && (
        <a
          href="#"
          onClick={() =>
            fetch("/log/individual", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ log: "Clicked link" }),
            })
          }
        >
          Click me
        </a>
      )}
    </>
  );
}
