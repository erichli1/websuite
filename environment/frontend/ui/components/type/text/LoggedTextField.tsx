import { log } from "@/ui/log";
import TextField, { TextFieldProps } from "@mui/material/TextField";
import React from "react";

export type LoggedTextFieldProps = Omit<TextFieldProps, "label" | "value"> & {
  logLabel: string;
  debounceMs?: number;
  hideLabel?: boolean;
};

export default function LoggedTextField(props: LoggedTextFieldProps) {
  const { logLabel, hideLabel, debounceMs, defaultValue, ...restProps } = props;

  const [value, setValue] = React.useState<string>(
    defaultValue !== undefined ? (defaultValue as string) : ""
  );
  const [lastCommittedValue, setLastCommittedValue] = React.useState<string>(
    defaultValue !== undefined ? (defaultValue as string) : ""
  );

  React.useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (lastCommittedValue !== value) {
        log({
          component: "type/text",
          label: logLabel,
          newVal: value,
          oldVal: lastCommittedValue,
        });
        setLastCommittedValue(value);
      }
    }, debounceMs ?? 500);

    return () => clearTimeout(delayDebounceFn);
  }, [lastCommittedValue, debounceMs, logLabel, value]);

  return (
    <TextField
      {...restProps}
      value={value}
      label={hideLabel ? undefined : logLabel}
      onChange={(event) => {
        setValue(event.target.value);
        props.onChange?.(event);
      }}
    />
  );
}
