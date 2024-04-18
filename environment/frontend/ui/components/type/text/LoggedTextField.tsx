import { log } from "@/ui/log";
import TextField, { TextFieldProps } from "@mui/material/TextField";
import React from "react";

export type LoggedTextFieldProps = Omit<TextFieldProps, "label"> & {
  logLabel: string;
  debounceMs?: number;
};

export default function LoggedTextField(props: LoggedTextFieldProps) {
  const { logLabel, debounceMs, defaultValue, ...restProps } = props;

  const [value, setValue] = React.useState<string>(
    defaultValue !== undefined ? (defaultValue as string) : ""
  );
  const [lastCommittedValue, setLastCommittedValue] = React.useState<string>(
    defaultValue !== undefined ? (defaultValue as string) : ""
  );

  React.useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (lastCommittedValue !== value)
        log({
          component: "type/text",
          label: logLabel,
          newVal: value,
          oldVal: lastCommittedValue,
        });
      setLastCommittedValue(value);
    }, props.debounceMs ?? 500);

    return () => clearTimeout(delayDebounceFn);
  }, [lastCommittedValue, props.debounceMs, logLabel, value]);

  return (
    <TextField
      {...restProps}
      value={value}
      label={logLabel}
      onChange={(event) => setValue(event.target.value)}
    />
  );
}
