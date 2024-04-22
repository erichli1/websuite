import Accordion, { AccordionProps } from "@mui/material/Accordion";
import AccordionDetails, {
  AccordionDetailsProps,
} from "@mui/material/AccordionDetails";
import AccordionSummary, {
  AccordionSummaryProps,
} from "@mui/material/AccordionSummary";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import React from "react";
import { log } from "@/ui/log";

export type LoggedAccordionProps = Omit<
  AccordionProps,
  "children" | "expanded"
> & {
  logLabel: string;
  summaryProps?: Omit<AccordionSummaryProps, "expandIcon">;
  details: React.ReactNode;
  detailsProps?: AccordionDetailsProps;
};

export default function LoggedAccordion(props: LoggedAccordionProps) {
  const { logLabel, summaryProps, details, detailsProps, ...restProps } = props;

  const [expanded, setExpanded] = React.useState(false);

  return (
    <Accordion
      {...restProps}
      expanded={expanded}
      onChange={(event, newExpanded) => {
        log({
          component: "click/accordion",
          label: logLabel,
          newVal: newExpanded ? "open" : "closed",
          oldVal: expanded ? "open" : "closed",
        }).then(() => {
          setExpanded(newExpanded);
          restProps.onChange?.(event, newExpanded);
        });
      }}
    >
      <AccordionSummary {...summaryProps} expandIcon={<ExpandMoreIcon />}>
        {logLabel}
      </AccordionSummary>
      <AccordionDetails {...detailsProps}>{details}</AccordionDetails>
    </Accordion>
  );
}
