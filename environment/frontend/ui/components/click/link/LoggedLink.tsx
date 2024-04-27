import { log, navigate } from "@/ui/log";
import Link, { LinkProps } from "@mui/material/Link";

export type LoggedLinkProps = LinkProps & {
  logLabel: string;
  afterLog?: () => void;
};

export default function LoggedLink(props: LoggedLinkProps) {
  const { logLabel, afterLog, ...restProps } = props;

  return (
    <Link
      {...restProps}
      onClick={(event) => {
        props.onClick?.(event);
        log({ component: "click/link", label: logLabel }).then(() => {
          if (afterLog) afterLog();
          if (props.href) navigate({ url: props.href });
        });
      }}
    >
      {logLabel}
    </Link>
  );
}
