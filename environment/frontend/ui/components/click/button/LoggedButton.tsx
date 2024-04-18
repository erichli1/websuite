import { log } from "@/ui/log";
import Button, { ButtonProps } from "@mui/material/Button";

export type LoggedButtonProps = ButtonProps & {
  logLabel: string;
};

export default function LoggedButton(props: LoggedButtonProps) {
  const { logLabel, ...restProps } = props;

  return (
    <Button
      {...restProps}
      onClick={(event) => {
        log({ component: "click/button", label: logLabel });
        props.onClick?.(event);
      }}
    >
      {logLabel}
    </Button>
  );
}
