import { log } from "@/ui/log";
import IconButton, { IconButtonProps } from "@mui/material/IconButton";
import React from "react";

export type LoggedIconButtonProps = IconButtonProps & {
  logLabel: string;
  icon: React.ReactNode;
  afterLog?: () => void;
};

export default function LoggedIconButton(props: LoggedIconButtonProps) {
  const { logLabel, afterLog, icon, ...restProps } = props;

  return (
    <IconButton
      {...restProps}
      {...{
        "aria-label": restProps["aria-label"] ?? logLabel,
      }}
      onClick={(event) => {
        props.onClick?.(event);
        log({ component: "click/iconbutton", label: logLabel }).then(() => {
          if (afterLog) afterLog();
        });
      }}
    >
      {icon}
    </IconButton>
  );
}
