import { Box, Typography } from "@mui/material";
import Slider, { SliderProps } from "@mui/material/Slider";
import React from "react";
import { log } from "@/ui/log";

export type LoggedSliderProps = SliderProps & {
  loglabel: string;
};

const STARTING_VAL = 30;

export default function LoggedSlider(props: LoggedSliderProps) {
  const [value, setValue] = React.useState<number>(
    (props.defaultValue as number) ?? STARTING_VAL
  );
  const [lastCommittedValue, setLastCommittedValue] = React.useState<number>(
    (props.defaultValue as number) ?? STARTING_VAL
  );

  return (
    <Box sx={{ width: 250 }}>
      <Typography>{props.loglabel}</Typography>
      <Slider
        {...props}
        value={value}
        onChange={(event, newValue, activeThumb) => {
          setValue(newValue as number);
          props.onChange?.(event, newValue, activeThumb);
        }}
        onChangeCommitted={(event, newValue) => {
          log({
            component: "click/slider",
            label: props.loglabel,
            newVal: newValue.toString(),
            oldVal: lastCommittedValue.toString(),
          });
          setLastCommittedValue(newValue as number);
          props.onChangeCommitted?.(event, newValue);
        }}
      />
    </Box>
  );
}
