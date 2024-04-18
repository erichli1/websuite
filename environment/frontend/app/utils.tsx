import LoggedButton from "@/ui/components/click/button/LoggedButton";
import LoggedLink from "@/ui/components/click/link/LoggedLink";
import LoggedSlider from "@/ui/components/click/slider/LoggedSlider";
import LoggedSnackbar from "@/ui/components/click/snackbar/LoggedSnackbar";
import React from "react";

export const ALL_TESTS: {
  [key: string]: {
    [key: string]: React.ReactNode;
  };
} = {
  click: {
    button: <LoggedButton loglabel="Submit" />,
    link: <LoggedLink loglabel="Settings" href="#" />,
    slider: <LoggedSlider loglabel="Volume" />,
    snackbar: <LoggedSnackbar loglabel="Message sent" />,
  },
};
