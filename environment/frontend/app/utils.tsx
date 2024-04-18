import LoggedButton from "@/ui/components/click/button/LoggedButton";
import LoggedLink from "@/ui/components/click/link/LoggedLink";
import LoggedSlider from "@/ui/components/click/slider/LoggedSlider";
import LoggedSnackbar from "@/ui/components/click/snackbar/LoggedSnackbar";
import LoggedSwitch from "@/ui/components/click/switch/LoggedSwitch";
import LoggedDatePicker from "@/ui/components/type/date/LoggedDatePicker";
import LoggedPhoneInput from "@/ui/components/type/phone/LoggedPhoneInput";
import LoggedTextField from "@/ui/components/type/text/LoggedTextField";
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
  },
  type: {
    text: <LoggedTextField logLabel="Name" defaultValue="" debounceMs={500} />,
    date: <LoggedDatePicker logLabel="Date" debounceMs={500} />,
    phone: <LoggedPhoneInput logLabel="Phone" debounceMs={500} />,
  },
};
