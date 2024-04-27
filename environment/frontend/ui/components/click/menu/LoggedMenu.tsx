import React from "react";
import Menu, { MenuProps } from "@mui/material/Menu";
import MenuItem, { MenuItemProps } from "@mui/material/MenuItem";
import { log } from "@/ui/log";

export type LoggedMenuProps = MenuProps & {
  menuItems: Array<LoggedMenuItemProps>;
  handleClose: () => void;
  afterLog?: () => void;
};

export type LoggedMenuItemProps = MenuItemProps & {
  logLabel: string;
};

export default function LoggedMenu(props: LoggedMenuProps) {
  const { menuItems, handleClose, afterLog, ...restProps } = props;

  return (
    <Menu
      {...restProps}
      onClose={(event, reason) => {
        handleClose();
        props.onClose?.(event, reason);
      }}
    >
      {menuItems.map((menuItem, index) => {
        const { logLabel, ...restMenuItemProps } = menuItem;
        return (
          <MenuItem
            key={index}
            {...restMenuItemProps}
            onClick={(event) => {
              menuItem.onClick?.(event);
              handleClose();

              log({
                component: "click/menu",
                label: logLabel,
              }).then(() => {
                if (afterLog) afterLog();
              });
            }}
          >
            {logLabel}
          </MenuItem>
        );
      })}
    </Menu>
  );
}
