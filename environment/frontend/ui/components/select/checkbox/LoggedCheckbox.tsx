import { log } from "@/ui/log";
import Checkbox, { CheckboxProps } from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import React from "react";

export type LoggedCheckboxProps = Omit<CheckboxProps, "checked"> & {
  logLabel: string;
};

export default function LoggedCheckbox(props: LoggedCheckboxProps) {
  const { logLabel, defaultChecked, ...restProps } = props;

  const [checked, setChecked] = React.useState(defaultChecked ?? false);

  return (
    <FormControlLabel
      control={
        <Checkbox
          {...restProps}
          checked={checked}
          onChange={(event, newChecked) => {
            log({
              component: "select/checkbox",
              label: logLabel,
              newVal: newChecked ? "true" : "false",
              oldVal: checked ? "true" : "false",
            });
            setChecked(newChecked);
            props.onChange?.(event, checked);
          }}
        />
      }
      label={logLabel}
    />
  );
}
