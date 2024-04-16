import { log } from "@/ui/log";
import Button, { ButtonProps } from "@mui/material/Button";

export type LoggedButtonProps = ButtonProps & {
  loglabel: string;
};

export default function LoggedButton(props: LoggedButtonProps) {
  return (
    <Button
      {...props}
      onClick={(event) => {
        log({ component: "click/button", label: props.loglabel });
        props.onClick?.(event);
      }}
    >
      {props.loglabel}
    </Button>
  );
}
