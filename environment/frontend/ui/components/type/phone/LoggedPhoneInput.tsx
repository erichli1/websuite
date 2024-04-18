import { log } from "@/ui/log";
import Input, { InputProps } from "@mui/material/Input";
import React from "react";
import { IMaskInput } from "react-imask";

export type LoggedPhoneInputProps = Omit<
  InputProps,
  "value" | "inputComponent"
> & {
  logLabel: string;
  debounceMs?: number;
};

type CustomProps = {
  onChange: (event: { target: { name: string; value: string } }) => void;
  name: string;
};

const TextMaskCustom = React.forwardRef<HTMLInputElement, CustomProps>(
  function TextMaskCustom(props, ref) {
    const { onChange, ...other } = props;
    return (
      <IMaskInput
        {...other}
        mask="(#00) 000-0000"
        definitions={{
          "#": /[1-9]/,
        }}
        inputRef={ref}
        onAccept={(value: any) =>
          onChange({ target: { name: props.name, value } })
        }
        overwrite
      />
    );
  }
);

export default function LoggedPhoneInput(props: LoggedPhoneInputProps) {
  const { logLabel, debounceMs, ...restProps } = props;

  const [value, setValue] = React.useState<string | null>(null);
  const [lastCommittedValue, setLastCommittedValue] = React.useState<
    string | null
  >(null);

  React.useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (lastCommittedValue !== value) {
        log({
          component: "type/phone",
          label: logLabel,
          newVal: value ?? "",
          oldVal: lastCommittedValue ?? "",
        });
        setLastCommittedValue(value);
      }
    }, debounceMs ?? 500);

    return () => clearTimeout(delayDebounceFn);
  }, [lastCommittedValue, debounceMs, logLabel, value]);

  return (
    <Input
      {...restProps}
      value={value}
      onChange={(event) => {
        setValue(event.target.value);
        props.onChange?.(event);
      }}
      inputComponent={TextMaskCustom as any}
    />
  );
}
