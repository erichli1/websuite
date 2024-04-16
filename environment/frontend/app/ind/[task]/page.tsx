"use client";

import { CLICK_TESTS, ClickTestType, TASKS } from "@/app/utils";
import LoggedButton from "@/ui/components/click/button/LoggedButton";
import LoggedLink from "@/ui/components/click/link/LoggedLink";
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
      {test === "button" && <LoggedButton loglabel="Click me" />}
      {test === "link" && <LoggedLink loglabel="Click me" href="#" />}
    </>
  );
}
