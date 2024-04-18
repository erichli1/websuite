import { log } from "@/ui/log";
import IconButton, { IconButtonProps } from "@mui/material/IconButton";
import React from "react";

export type LoggedIconButtonProps = IconButtonProps & {
  logLabel: string;
  icon: React.ReactNode;
};

export default function LoggedIconButton(props: LoggedIconButtonProps) {
  const { logLabel, icon, ...restProps } = props;

  return (
    <IconButton
      {...restProps}
      onClick={(event) => {
        log({ component: "click/iconbutton", label: logLabel });
        props.onClick?.(event);
      }}
    >
      {icon}
    </IconButton>
  );
}
