import { Box, Stack } from "@mui/material";
import LoggedTextField from "../components/type/text/LoggedTextField";
import LoggedPhoneInput from "../components/type/phone/LoggedPhoneInput";
import LoggedSelect from "../components/select/select/LoggedSelect";
import LoggedDatePicker from "../components/type/date/LoggedDatePicker";

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
  fields: Array<Field | Array<Field>>;
};

export function FormContainer(props: FormContainerProps) {
  return (
    <Stack maxWidth="md" sx={{ marginX: "auto", padding: "1rem" }} spacing={2}>
      {props.fields.map((field, index) =>
        Array.isArray(field) ? (
          <Stack
            direction="row"
            spacing={2}
            useFlexGap
            key={`form-container-${index}`}
          >
            {field.map((subField, subIndex) => (
              <Box key={`form-container-${index}-${subIndex}`} flexGrow={1}>
                <MetaFormComponent field={subField} />
              </Box>
            ))}
          </Stack>
        ) : (
          <MetaFormComponent field={field} key={`form-container-${index}`} />
        )
      )}
    </Stack>
  );
}

function MetaFormComponent({ field }: { field: Field }) {
  switch (field) {
    case "firstName":
      return <LoggedTextField logLabel="First name" fullWidth />;
    case "lastName":
      return <LoggedTextField logLabel="Last name" fullWidth />;
    case "phoneNumber":
      return <LoggedPhoneInput logLabel="Phone number" fullWidth />;
    case "email":
      return <LoggedTextField logLabel="Email" fullWidth />;
    case "streetAddress":
      return <LoggedTextField logLabel="Street address" fullWidth />;
    case "city":
      return <LoggedTextField logLabel="City" fullWidth />;
    case "state":
      return <SelectState />;
    case "zipCode":
      return <LoggedTextField logLabel="Zip code" fullWidth />;
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
      fullWidth
    />
  );
}
