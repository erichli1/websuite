import LoggedButton from "@/ui/components/click/button/LoggedButton";
import LoggedConfirmButton from "@/ui/components/click/confirmbutton/LoggedConfirmButton";
import LoggedIconButton from "@/ui/components/click/iconbutton/LoggedIconButton";
import LoggedLink from "@/ui/components/click/link/LoggedLink";
import LoggedSlider from "@/ui/components/click/slider/LoggedSlider";
import LoggedSnackbar from "@/ui/components/click/snackbar/LoggedSnackbar";
import LoggedSwitch from "@/ui/components/click/switch/LoggedSwitch";
import LoggedCheckbox from "@/ui/components/select/checkbox/LoggedCheckbox";
import LoggedSelect from "@/ui/components/select/select/LoggedSelect";
import LoggedDatePicker from "@/ui/components/type/date/LoggedDatePicker";
import LoggedPhoneInput from "@/ui/components/type/phone/LoggedPhoneInput";
import LoggedTextField from "@/ui/components/type/text/LoggedTextField";
import { Delete } from "@mui/icons-material";
import { Box, FormGroup } from "@mui/material";
import React from "react";
import {
  DefaultMenuContainer,
  DropdownMenuContainer,
} from "../ui/containers/Menus";
import { AppBarContainer } from "@/ui/containers/Appbars";
import DataGridContainer from "@/ui/containers/DataGrids";

export const ALL_TESTS: {
  [key: string]: {
    [key: string]: React.ReactNode;
  };
} = {
  click: {
    button: <LoggedButton logLabel="Submit" />,
    confirmbutton: (
      <LoggedConfirmButton
        logLabel="Delete"
        dialog={{ title: "Are you sure?" }}
        confirm={{ label: "Yes" }}
        cancel={{ label: "No" }}
      />
    ),
    iconbutton: <LoggedIconButton logLabel="Delete" icon={<Delete />} />,
    link: <LoggedLink logLabel="Settings" href="#" />,
    slider: <LoggedSlider logLabel="Volume" defaultValue={30} />,
    snackbar: <LoggedSnackbar logLabel="Message sent" />,
    switch: <LoggedSwitch logLabel="Do not disturb" defaultChecked={false} />,
    dropdownmenu: (
      <AppBarContainer title="News">
        <DropdownMenuContainer
          logLabel="Menu"
          items={["Profile", "Settings", "Log out"]}
        />
      </AppBarContainer>
    ),
  },
  type: {
    text: <LoggedTextField logLabel="Name" defaultValue="" debounceMs={500} />,
    date: <LoggedDatePicker logLabel="Date" debounceMs={500} />,
    phone: <LoggedPhoneInput logLabel="Phone" debounceMs={500} />,
  },
  select: {
    checkbox: <LoggedCheckbox logLabel="I accept the terms and conditions" />,
    multicheck: (
      <FormGroup>
        <LoggedCheckbox logLabel="I accept the terms and conditions" />
        <LoggedCheckbox logLabel="I understand the privacy policy" />
      </FormGroup>
    ),
    select: (
      <Box sx={{ width: 250 }}>
        <LoggedSelect
          logLabel="Country"
          menuItems={[
            { label: "USA" },
            { label: "Canada" },
            { label: "Mexico" },
          ]}
        />
      </Box>
    ),
    grid: (
      <DataGridContainer<{
        name: string;
        country: string;
        orderDate: string;
      }>
        columns={[
          { field: "name", headerName: "Name" },
          { field: "country", headerName: "Country" },
          { field: "orderDate", headerName: "Order Date" },
        ]}
        gridLogLabel="Orders"
        rows={[
          {
            name: "John Doe",
            country: "USA",
            orderDate: "2024-01-02",
            id: "1",
            logLabel: "John Doe",
          },
          {
            name: "Jane Smith",
            country: "Canada",
            orderDate: "2024-01-11",
            id: "2",
            logLabel: "Jane Smith",
          },
          {
            name: "Alice Johnson",
            country: "UK",
            orderDate: "2024-01-04",
            id: "3",
            logLabel: "Alice Johnson",
          },
          {
            name: "Bob Brown",
            country: "Australia",
            orderDate: "2024-01-06",
            id: "4",
            logLabel: "Bob Brown",
          },
          {
            name: "Mary Davis",
            country: "Germany",
            orderDate: "2024-01-06",
            id: "5",
            logLabel: "Mary Davis",
          },
          {
            name: "Tom Wilson",
            country: "France",
            orderDate: "2024-01-05",
            id: "6",
            logLabel: "Tom Wilson",
          },
          {
            name: "Sara Moore",
            country: "Spain",
            orderDate: "2024-01-10",
            id: "7",
            logLabel: "Sara Moore",
          },
          {
            name: "James Taylor",
            country: "Italy",
            orderDate: "2024-01-11",
            id: "8",
            logLabel: "James Taylor",
          },
          {
            name: "Patricia White",
            country: "Netherlands",
            orderDate: "2024-01-01",
            id: "9",
            logLabel: "Patricia White",
          },
          {
            name: "Michael Harris",
            country: "Sweden",
            orderDate: "2024-01-08",
            id: "10",
            logLabel: "Michael Harris",
          },
        ]}
      />
    ),
  },
  menu: {
    basic: (
      <AppBarContainer title="Menu">
        <DefaultMenuContainer items={["Profile", "Settings", "Log out"]} />
      </AppBarContainer>
    ),
    nested: (
      <AppBarContainer title="Menu">
        <DefaultMenuContainer
          items={[
            "Profile",
            {
              label: "Settings",
              subitems: [
                "Account preferences",
                "Sign in & security",
                "Visibility",
                "Data privacy",
                "Notifications",
              ],
            },
            "Log out",
          ]}
        />
      </AppBarContainer>
    ),
  },
};
