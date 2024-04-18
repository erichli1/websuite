import { log } from "@/ui/log";
import TextField, { TextFieldProps } from "@mui/material/TextField";
import React from "react";

export type LoggedTextFieldProps = Omit<TextFieldProps, "label"> & {
  loglabel: string;
  debounceMs?: number;
};

export default function LoggedTextField(props: LoggedTextFieldProps) {
  const { debounceMs, defaultValue, ...restProps } = props;

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
          label: props.loglabel,
          newVal: value,
          oldVal: lastCommittedValue,
        });
      setLastCommittedValue(value);
    }, props.debounceMs ?? 500);

    return () => clearTimeout(delayDebounceFn);
  }, [lastCommittedValue, props.debounceMs, props.loglabel, value]);

  return (
    <TextField
      {...restProps}
      value={value}
      label={props.loglabel}
      onChange={(event) => setValue(event.target.value)}
    />
  );
}
