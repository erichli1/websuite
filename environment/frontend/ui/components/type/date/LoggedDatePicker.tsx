import { DatePicker, DatePickerProps } from "@mui/x-date-pickers/DatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { Dayjs } from "dayjs";
import React from "react";
import { log } from "@/ui/log";

type LoggedDatePickerProps<
  TInputDate extends Dayjs,
  TDate extends boolean
> = Omit<DatePickerProps<TInputDate, TDate>, "value"> & {
  logLabel: string;
  debounceMs?: number;
};

export default function LoggedDatePicker(
  props: LoggedDatePickerProps<Dayjs, boolean>
) {
  const { logLabel, defaultValue, debounceMs, ...restProps } = props;

  const [value, setValue] = React.useState<Dayjs | null>(defaultValue ?? null);
  const [lastCommittedValue, setLastCommittedValue] =
    React.useState<Dayjs | null>(defaultValue ?? null);

  React.useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (lastCommittedValue !== value) {
        log({
          component: "type/date",
          label: logLabel,
          newVal: value?.toString() ?? "",
          oldVal: lastCommittedValue?.toString() ?? "",
        });
        setLastCommittedValue(value);
      }
    }, debounceMs ?? 500);

    return () => clearTimeout(delayDebounceFn);
  }, [lastCommittedValue, debounceMs, logLabel, value]);

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker
        {...restProps}
        label={logLabel}
        value={value}
        onChange={(newValue, context) => {
          setValue(newValue);
          props.onChange?.(newValue, context);
        }}
      />
    </LocalizationProvider>
  );
}
