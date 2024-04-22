import IconButton from "@mui/material/IconButton";
import Snackbar, { SnackbarProps } from "@mui/material/Snackbar";
import React from "react";
import CloseIcon from "@mui/icons-material/Close";
import { log } from "@/ui/log";

export type LoggedSnackbarProps = Omit<
  SnackbarProps,
  "open" | "message" | "action"
> & {
  logLabel: string;
};

export default function LoggedSnackbar(props: LoggedSnackbarProps) {
  const { logLabel, ...restProps } = props;
  const [open, setOpen] = React.useState(true);

  const handleClose = (
    _event: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === "clickaway") {
      return;
    }

    setOpen(false);
  };

  return (
    <Snackbar
      {...restProps}
      open={open}
      onClose={(event, reason) => {
        handleClose(event, reason);
        props.onClose?.(event, reason);
      }}
      message={logLabel}
      action={
        <IconButton
          size="small"
          aria-label="close"
          color="inherit"
          onClick={(event) => {
            log({
              component: "click/snackbar",
              label: logLabel,
              newVal: "closed",
              oldVal: "open",
            }).then(() => {
              handleClose(event);
            });
          }}
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      }
    />
  );
}
