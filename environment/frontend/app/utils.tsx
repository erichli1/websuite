import LoggedButton from "@/ui/components/click/button/LoggedButton";
import LoggedLink from "@/ui/components/click/link/LoggedLink";
import LoggedMenu from "@/ui/components/click/menu/LoggedMenu";
import LoggedSlider from "@/ui/components/click/slider/LoggedSlider";
import LoggedSnackbar from "@/ui/components/click/snackbar/LoggedSnackbar";
import LoggedSwitch from "@/ui/components/click/switch/LoggedSwitch";
import LoggedCheckbox from "@/ui/components/select/checkbox/LoggedCheckbox";
import LoggedDatePicker from "@/ui/components/type/date/LoggedDatePicker";
import LoggedPhoneInput from "@/ui/components/type/phone/LoggedPhoneInput";
import LoggedTextField from "@/ui/components/type/text/LoggedTextField";
import FormGroup from "@mui/material/FormGroup";
import React from "react";

export const ALL_TESTS: {
  [key: string]: {
    [key: string]: React.ReactNode;
  };
} = {
  click: {
    button: <LoggedButton logLabel="Submit" />,
    link: <LoggedLink logLabel="Settings" href="#" />,
    slider: <LoggedSlider logLabel="Volume" defaultValue={30} />,
    snackbar: <LoggedSnackbar logLabel="Message sent" />,
    switch: <LoggedSwitch logLabel="Do not disturb" defaultChecked={false} />,
    menu: (
      <LoggedMenu
        menuItems={[
          { logLabel: "Profile" },
          { logLabel: "Settings" },
          { logLabel: "Log out" },
        ]}
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
  },
};
