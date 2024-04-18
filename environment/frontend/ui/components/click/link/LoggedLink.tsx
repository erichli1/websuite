import { log } from "@/ui/log";
import Link, { LinkProps } from "@mui/material/Link";

export type LoggedLinkProps = LinkProps & {
  logLabel: string;
};

export default function LoggedLink(props: LoggedLinkProps) {
  const { logLabel, ...restProps } = props;

  return (
    <Link
      {...restProps}
      onClick={(event) => {
        log({ component: "click/link", label: logLabel });
        props.onClick?.(event);
      }}
    >
      {logLabel}
    </Link>
  );
}
