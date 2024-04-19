import LoggedButton from "@/ui/components/click/button/LoggedButton";
import LoggedMenu from "@/ui/components/click/menu/LoggedMenu";
import { Typography } from "@mui/material";
import React from "react";
import LoggedIconButton from "../components/click/iconbutton/LoggedIconButton";
import MenuIcon from "@mui/icons-material/Menu";

export function DefaultMenuContainer({
  items,
}: {
  items: Array<
    | string
    | {
        label: string;
        subitems: Array<string>;
      }
  >;
}) {
  return (
    <>
      {items.map((item, index) => {
        if (typeof item === "string")
          return (
            <LoggedButton
              key={`menu-l1-${index}`}
              color="inherit"
              logLabel={item}
            />
          );
        else if (typeof item === "object")
          return (
            <NestedMenuButton
              key={`menu-l1-${index}`}
              items={item.subitems}
              label={item.label}
            />
          );
      })}
    </>
  );
}

function NestedMenuButton({
  label,
  items,
}: {
  label: string;
  items: Array<string>;
}) {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  return (
    <div>
      <LoggedButton
        color="inherit"
        logLabel={label}
        onClick={(event) => {
          setAnchorEl(event.currentTarget);
        }}
      />
      <LoggedMenu
        anchorEl={anchorEl}
        open={open}
        handleClose={() => {
          setAnchorEl(null);
        }}
        menuItems={items.map((item) => ({
          logLabel: item,
          color: "inherit",
        }))}
      />
    </div>
  );
}

export function DropdownMenuContainer({
  logLabel,
  items,
}: {
  logLabel: string;
  items: Array<string>;
}) {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  return (
    <>
      <LoggedIconButton
        size="large"
        edge="start"
        color="inherit"
        onClick={(event) => {
          setAnchorEl(event.currentTarget);
        }}
        logLabel={logLabel}
        icon={<MenuIcon />}
      />
      <LoggedMenu
        anchorEl={anchorEl}
        open={open}
        handleClose={() => {
          setAnchorEl(null);
        }}
        menuItems={items.map((item) => ({
          logLabel: item,
          color: "inherit",
        }))}
      />
    </>
  );
}
