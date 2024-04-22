import { Box, Typography } from "@mui/material";
import Slider, { SliderProps } from "@mui/material/Slider";
import React from "react";
import { log } from "@/ui/log";

export type LoggedSliderProps = SliderProps & {
  logLabel: string;
};

const STARTING_VAL = 30;

export default function LoggedSlider(props: LoggedSliderProps) {
  const { logLabel, defaultValue, ...restProps } = props;

  const [value, setValue] = React.useState<number>(
    (defaultValue as number) ?? STARTING_VAL
  );
  const [lastCommittedValue, setLastCommittedValue] = React.useState<number>(
    (defaultValue as number) ?? STARTING_VAL
  );

  return (
    <Box sx={{ width: 250 }}>
      <Typography>{logLabel}</Typography>
      <Slider
        {...restProps}
        value={value}
        onChange={(event, newValue, activeThumb) => {
          setValue(newValue as number);
          props.onChange?.(event, newValue, activeThumb);
        }}
        onChangeCommitted={(event, newValue) => {
          log({
            component: "click/slider",
            label: logLabel,
            newVal: newValue.toString(),
            oldVal: lastCommittedValue.toString(),
          }).then(() => {
            setLastCommittedValue(newValue as number);
            props.onChangeCommitted?.(event, newValue);
          });
        }}
      />
    </Box>
  );
}
