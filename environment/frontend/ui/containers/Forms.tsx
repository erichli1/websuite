import { Stack } from "@mui/material";
import LoggedTextField from "../components/type/text/LoggedTextField";
import LoggedPhoneInput from "../components/type/phone/LoggedPhoneInput";
import LoggedSelect from "../components/select/select/LoggedSelect";
import LoggedDatePicker from "../components/type/date/LoggedDatePicker";

// TODO: add more fields
// TODO: support fields being stored in a grid format (eg: Field | Array<Field>)

type Field =
  | "firstName"
  | "lastName"
  | "phoneNumber"
  | "email"
  | "streetAddress"
  | "city"
  | "state"
  | "zipCode"
  | "birthday";

export type FormContainerProps = {
  fields: Array<Field>;
};

export function FormContainer(props: FormContainerProps) {
  return (
    <Stack maxWidth="md" sx={{ marginX: "auto", padding: "1rem" }} spacing={2}>
      {props.fields.map((field, index) => (
        <MetaFormComponent field={field} key={`form-container-${index}`} />
      ))}
    </Stack>
  );
}

function MetaFormComponent({ field }: { field: Field }) {
  switch (field) {
    case "firstName":
      return <LoggedTextField logLabel="First name" />;
    case "lastName":
      return <LoggedTextField logLabel="Last name" />;
    case "phoneNumber":
      return <LoggedPhoneInput logLabel="Phone number" />;
    case "email":
      return <LoggedTextField logLabel="Email" />;
    case "streetAddress":
      return <LoggedTextField logLabel="Street address" />;
    case "city":
      return <LoggedTextField logLabel="City" />;
    case "state":
      return <SelectState />;
    case "zipCode":
      return <LoggedTextField logLabel="Zip code" />;
    case "birthday":
      return <LoggedDatePicker logLabel="Birthday" />;
    default:
      const exhaustiveCheck: never = field;
      throw new Error(`Unhandled case: ${exhaustiveCheck}`);
  }
}

function SelectState() {
  return (
    <LoggedSelect
      logLabel="State"
      menuItems={[
        { label: "AL" },
        { label: "AK" },
        { label: "AZ" },
        { label: "AR" },
        { label: "CA" },
        { label: "CO" },
        { label: "CT" },
        { label: "DE" },
        { label: "FL" },
        { label: "GA" },
        { label: "HI" },
        { label: "ID" },
        { label: "IL" },
        { label: "IN" },
        { label: "IA" },
        { label: "KS" },
        { label: "KY" },
        { label: "LA" },
        { label: "ME" },
        { label: "MD" },
        { label: "MA" },
        { label: "MI" },
        { label: "MN" },
        { label: "MS" },
        { label: "MO" },
        { label: "MT" },
        { label: "NE" },
        { label: "NV" },
        { label: "NH" },
        { label: "NJ" },
        { label: "NM" },
        { label: "NY" },
        { label: "NC" },
        { label: "ND" },
        { label: "OH" },
        { label: "OK" },
        { label: "OR" },
        { label: "PA" },
        { label: "RI" },
        { label: "SC" },
        { label: "SD" },
        { label: "TN" },
        { label: "TX" },
        { label: "UT" },
        { label: "VT" },
        { label: "VA" },
        { label: "WA" },
        { label: "WV" },
        { label: "WI" },
        { label: "WY" },
      ]}
    />
  );
}
