import Switch, { SwitchProps } from "@mui/material/Switch";
import FormControlLabel from "@mui/material/FormControlLabel";
import React from "react";
import { log } from "@/ui/log";

export type LoggedSwitchProps = SwitchProps & {
  logLabel: string;
};

export default function LoggedSwitch(props: LoggedSwitchProps) {
  const { logLabel, ...restProps } = props;
  const [checked, setChecked] = React.useState(props.defaultChecked ?? false);

  return (
    <FormControlLabel
      control={
        <Switch
          {...restProps}
          onChange={(event, newChecked) => {
            setChecked(newChecked);
            log({
              component: "click/switch",
              label: logLabel,
              newVal: newChecked ? "on" : "off",
              oldVal: checked ? "on" : "off",
            });
            props.onChange?.(event, checked);
          }}
        />
      }
      label={logLabel}
    />
  );
}
