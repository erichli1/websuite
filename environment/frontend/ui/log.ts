export function log({
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
  fetch("/log", {
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
