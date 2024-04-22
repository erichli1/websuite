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
import { NAME_COUNTRY_ORDERDATE_ROWS } from "./data";
import {
  BasicInfo,
  InfoAccordion,
  InfoDialog,
  InfoTooltip,
} from "@/ui/containers/FindInfos";
import LoggedAccordion from "@/ui/components/click/accordion/LoggedAccordion";
import { FormContainer } from "@/ui/containers/Forms";

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
    accordion: (
      <LoggedAccordion
        logLabel="See more"
        details="This is more information about the topic!"
      />
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
        rows={NAME_COUNTRY_ORDERDATE_ROWS}
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
  info: {
    gridfilter: (
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
        rows={NAME_COUNTRY_ORDERDATE_ROWS}
      />
    ),
    gridsort: (
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
        rows={NAME_COUNTRY_ORDERDATE_ROWS}
      />
    ),
    findbasic: <BasicInfo />,
    findtooltip: <InfoTooltip />,
    finddialog: <InfoDialog />,
    findaccordion: <InfoAccordion />,
  },
  fill: {
    basicform: <FormContainer fields={["firstName", "lastName", "email"]} />,
  },
};
