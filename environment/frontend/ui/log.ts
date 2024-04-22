export async function log({
  component,
  label,
  newVal,
  oldVal,
}: {
  component: string;
  label: string;
  newVal?: string;
  oldVal?: string;
}) {
  await fetch("/log", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      log: `${component} // ${label}${
        newVal !== undefined ? " // " + newVal : ""
      }${oldVal !== undefined ? " // " + oldVal : ""}`,
    }),
  });
}

export async function submit({ input }: { input: string }) {
  await fetch("/log", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      log: `SUBMIT // ${input}`,
    }),
  });
}

export function stringifyJsonSortKeys(obj: any) {
  return JSON.stringify(obj, Object.keys(obj).sort());
}

export async function navigate({ url }: { url: string }) {
  await fetch("/log", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      log: `NAVIGATE // ${url}`,
    }),
  });
}
