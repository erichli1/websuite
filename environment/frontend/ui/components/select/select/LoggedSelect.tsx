import Select, { SelectProps } from "@mui/material/Select";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import MenuItem, { MenuItemProps } from "@mui/material/MenuItem";
import React from "react";
import Box from "@mui/material/Box";
import { log } from "@/ui/log";

export type LoggedSelectProps = Omit<SelectProps, "value" | "label"> & {
  logLabel: string;
  menuItems: Array<Omit<MenuItemProps, "key" | "value"> & { label: string }>;
};

export default function LoggedSelect(props: LoggedSelectProps) {
  const { logLabel, menuItems, ...restProps } = props;

  const [value, setValue] = React.useState<string>("");

  return (
    <FormControl sx={{ width: "100%" }}>
      <InputLabel>{logLabel}</InputLabel>
      <Select
        {...restProps}
        value={value}
        label={logLabel}
        onChange={(event, child) => {
          log({
            component: "select/select",
            label: logLabel,
            newVal: event.target.value as string,
            oldVal: value,
          });
          setValue(event.target.value as string);
          props.onChange?.(event, child);
        }}
      >
        {menuItems.map(({ label, ...restMenuItemProps }, index) => (
          <MenuItem
            {...restMenuItemProps}
            key={`select-${label}-${index}`}
            value={label}
          >
            {label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
