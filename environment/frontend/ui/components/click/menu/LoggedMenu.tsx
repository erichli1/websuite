import IconButton from "@mui/material/IconButton";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import MenuIcon from "@mui/icons-material/Menu";
import React from "react";
import Menu, { MenuProps } from "@mui/material/Menu";
import MenuItem, { MenuItemProps } from "@mui/material/MenuItem";
import Typography from "@mui/material/Typography";
import { log } from "@/ui/log";

export type LoggedMenuProps = Omit<MenuProps, "anchorEl" | "open"> & {
  menuItems: Array<LoggedMenuItemProps>;
};

export type LoggedMenuItemProps = Omit<MenuItemProps, "key"> & {
  logLabel: string;
};

export default function LoggedMenu(props: LoggedMenuProps) {
  const { menuItems, ...restProps } = props;

  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          News
        </Typography>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          onClick={(event) => {
            setAnchorEl(event.currentTarget);
          }}
        >
          <MenuIcon />
        </IconButton>
        <Menu
          {...restProps}
          anchorEl={anchorEl}
          open={open}
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
                  log({
                    component: "click/menu",
                    label: logLabel,
                  });
                  menuItem.onClick?.(event);
                  handleClose();
                }}
              >
                {logLabel}
              </MenuItem>
            );
          })}
        </Menu>
      </Toolbar>
    </AppBar>
  );
}