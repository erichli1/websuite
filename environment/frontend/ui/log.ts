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

function deepSortObject(obj: any) {
  if (typeof obj !== "object" || obj === null) {
    return obj;
  }

  const keys = Object.keys(obj).sort();
  const newObj: { [key: string]: any } = {};
  for (const key of keys) {
    newObj[key] = deepSortObject(obj[key]); // Recursive sorting
  }
  return newObj;
}

export function stringifyJsonSortKeys(obj: any) {
  const sorted_obj = deepSortObject(obj);
  return JSON.stringify(sorted_obj);
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
