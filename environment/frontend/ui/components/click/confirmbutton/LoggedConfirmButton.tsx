import { log } from "@/ui/log";
import Button, { ButtonProps } from "@mui/material/Button";
import Dialog, { DialogProps } from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogTitle from "@mui/material/DialogTitle";
import React from "react";

export type LoggedDialogButtonProps = {
  logLabel: string;
  button?: ButtonProps;
  dialog: Omit<DialogProps, "open"> & { title: string };
  confirm: ButtonProps & { label: string };
  cancel: ButtonProps & { label: string };
};

export default function LoggedConfirmButton(props: LoggedDialogButtonProps) {
  const { logLabel, button, dialog, confirm, cancel, ...restProps } = props;
  const { label: confirmLabel, ...restConfirmProps } = confirm;
  const { label: cancelLabel, ...restCancelProps } = cancel;

  const [open, setOpen] = React.useState(false);

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Button
        onClick={(event) => {
          setOpen(true);
          button?.onClick?.(event);
        }}
      >
        {logLabel}
      </Button>
      <Dialog
        open={open}
        onClose={(event, reason) => {
          handleClose();
          dialog.onClose?.(event, reason);
        }}
      >
        <DialogTitle>{dialog.title}</DialogTitle>
        <DialogActions>
          <Button
            {...restConfirmProps}
            onClick={(event) => {
              log({
                component: "click/confirmbutton",
                label: logLabel,
              }).then(() => {
                confirm.onClick?.(event);
                handleClose();
              });
            }}
          >
            {confirmLabel}
          </Button>
          <Button
            {...restCancelProps}
            onClick={(event) => {
              cancel.onClick?.(event);
              handleClose();
            }}
          >
            {cancelLabel}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
