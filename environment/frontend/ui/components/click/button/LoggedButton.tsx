import { log } from "@/ui/log";
import Button, { ButtonProps } from "@mui/material/Button";

export type LoggedButtonProps = ButtonProps & {
  logLabel: string;
  afterLog?: () => void;
};

export default function LoggedButton(props: LoggedButtonProps) {
  const { logLabel, afterLog, ...restProps } = props;

  return (
    <Button
      {...restProps}
      onClick={(event) => {
        props.onClick?.(event);
        log({ component: "click/button", label: logLabel }).then(() => {
          if (afterLog) afterLog();
        });
      }}
    >
      {logLabel}
    </Button>
  );
}
