import { log } from "@/ui/log";
import Link, { LinkProps } from "@mui/material/Link";

export type LoggedLinkProps = LinkProps & {
  loglabel: string;
};

export default function LoggedLink(props: LoggedLinkProps) {
  return (
    <Link
      {...props}
      onClick={(event) => {
        log({ component: "click/link", label: props.loglabel });
        props.onClick?.(event);
      }}
    >
      {props.loglabel}
    </Link>
  );
}
