import { Box, Stack } from "@mui/material";
import LoggedTextField from "../components/type/text/LoggedTextField";
import LoggedPhoneInput from "../components/type/phone/LoggedPhoneInput";
import LoggedSelect from "../components/select/select/LoggedSelect";
import LoggedDatePicker from "../components/type/date/LoggedDatePicker";
import React from "react";
import LoggedButton from "../components/click/button/LoggedButton";
import { stringifyJsonSortKeys, submit } from "../log";

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
  submitLabel: string;
  onSubmit?: (formValuesString: string) => void;
  dontLogSubmit?: boolean;
};

export function FormContainer(props: FormContainerProps) {
  const [formValues, setFormValues] = React.useState<{ [key: string]: string }>(
    {}
  );

  const updateFormValues = (key: string, value: string) => {
    setFormValues((prev) => ({ ...prev, [key]: value }));
  };

  React.useEffect(() => {
    props.fields.forEach((field) => {
      if (Array.isArray(field)) {
        field.forEach((subField) => {
          updateFormValues(subField, "");
        });
      } else {
        updateFormValues(field, "");
      }
    });
  }, [props.fields]);

  return (
    <Stack maxWidth="md" sx={{ marginX: "auto" }} spacing={2}>
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
                <MetaFormComponent
                  field={subField}
                  updateFormValues={updateFormValues}
                />
              </Box>
            ))}
          </Stack>
        ) : (
          <MetaFormComponent
            field={field}
            key={`form-container-${index}`}
            updateFormValues={updateFormValues}
          />
        )
      )}
      <div>
        <LoggedButton
          logLabel={props.submitLabel}
          onClick={() => {
            if (props.dontLogSubmit)
              props.onSubmit?.(stringifyJsonSortKeys(formValues));
            else
              submit({ input: stringifyJsonSortKeys(formValues) }).then(() => {
                props.onSubmit?.(stringifyJsonSortKeys(formValues));
              });
          }}
          variant="contained"
        />
      </div>
    </Stack>
  );
}

function MetaFormComponent({
  field,
  updateFormValues,
}: {
  field: Field;
  updateFormValues: (key: string, value: string) => void;
}) {
  switch (field) {
    case "firstName":
      return (
        <LoggedTextField
          logLabel="First name"
          fullWidth
          onChange={(event) => updateFormValues(field, event.target.value)}
        />
      );
    case "lastName":
      return (
        <LoggedTextField
          logLabel="Last name"
          fullWidth
          onChange={(event) => updateFormValues(field, event.target.value)}
        />
      );
    case "phoneNumber":
      return (
        <LoggedPhoneInput
          logLabel="Phone number"
          fullWidth
          onChange={(event) => updateFormValues(field, event.target.value)}
        />
      );
    case "email":
      return (
        <LoggedTextField
          logLabel="Email"
          fullWidth
          onChange={(event) => updateFormValues(field, event.target.value)}
        />
      );
    case "streetAddress":
      return (
        <LoggedTextField
          logLabel="Street address"
          fullWidth
          onChange={(event) => updateFormValues(field, event.target.value)}
        />
      );
    case "city":
      return (
        <LoggedTextField
          logLabel="City"
          fullWidth
          onChange={(event) => updateFormValues(field, event.target.value)}
        />
      );
    case "state":
      return <SelectState field={field} updateFormValues={updateFormValues} />;
    case "zipCode":
      return (
        <LoggedTextField
          logLabel="Zip code"
          fullWidth
          onChange={(event) => updateFormValues(field, event.target.value)}
        />
      );
    case "birthday":
      return (
        <LoggedDatePicker
          logLabel="Birthday"
          onChange={(value) => updateFormValues(field, value?.toString() ?? "")}
        />
      );
    default:
      const exhaustiveCheck: never = field;
      throw new Error(`Unhandled case: ${exhaustiveCheck}`);
  }
}

function SelectState({
  field,
  updateFormValues,
}: {
  field: Field;
  updateFormValues: (key: string, value: string) => void;
}) {
  return (
    <LoggedSelect
      logLabel="State"
      onChange={(event) =>
        updateFormValues(field, event.target.value as string)
      }
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
