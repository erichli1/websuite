import LoggedButton from "@/ui/components/click/button/LoggedButton";
import LoggedLink from "@/ui/components/click/link/LoggedLink";
import LoggedSlider from "@/ui/components/click/slider/LoggedSlider";
import LoggedSnackbar from "@/ui/components/click/snackbar/LoggedSnackbar";
import LoggedSwitch from "@/ui/components/click/switch/LoggedSwitch";
import LoggedTextField from "@/ui/components/type/text/LoggedTextField";
import React from "react";

export const ALL_TESTS: {
  [key: string]: {
    [key: string]: React.ReactNode;
  };
} = {
  click: {
    button: <LoggedButton loglabel="Submit" />,
    link: <LoggedLink loglabel="Settings" href="#" />,
    slider: <LoggedSlider loglabel="Volume" defaultValue={30} />,
    snackbar: <LoggedSnackbar loglabel="Message sent" />,
    switch: <LoggedSwitch loglabel="Do not disturb" defaultChecked={false} />,
  },
  type: {
    text: <LoggedTextField loglabel="Name" defaultValue="" debounceMs={500} />,
  },
};
