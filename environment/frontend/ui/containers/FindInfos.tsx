import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Dialog,
  DialogContent,
  DialogTitle,
  Stack,
  Tooltip,
  Typography,
} from "@mui/material";
import LoggedTextField from "../components/type/text/LoggedTextField";
import { Info } from "@mui/icons-material";
import LoggedButton from "../components/click/button/LoggedButton";
import React from "react";
import LoggedAccordion from "../components/click/accordion/LoggedAccordion";

function IntroParagraph({ tooltipText }: { tooltipText?: boolean }) {
  return (
    <Typography variant="body1">
      AGI Research Lab is a fictional multinational technology company
      headquartered in Aurora City
      {tooltipText ? (
        <sup>
          <Tooltip title="Aurora City is located in California and was founded in 2025.">
            <Info sx={{ height: "1rem", width: "1rem" }} />
          </Tooltip>
        </sup>
      ) : (
        ""
      )}
      , founded in 2032 by a group of innovators and scientists dedicated to
      advancing the field of artificial general intelligence (AGI). The company
      specializes in developing AGI systems that can perform any intellectual
      task that a human being can. AGI Research Lab aims to create AI that can
      reason, solve problems, and understand emotions at a human level.
    </Typography>
  );
}

function PrometheusParagraph({
  learnMoreDialog,
}: {
  learnMoreDialog?: boolean;
}) {
  const [open, setOpen] = React.useState(false);

  return (
    <>
      <Typography variant="body1">
        A few years after being founded, the company&apos;s major breakthrough
        came with the development of &quot;Prometheus&quot;, a prototype AGI
        system capable of learning independently from its environment.
        Prometheus was designed to adapt to various industries, ranging from
        healthcare to finance, significantly outperforming existing AI in
        complex cognitive tasks. This innovation positioned AGI Research Lab as
        a leader in AGI technology, attracting attention from global tech giants
        and governments alike.
      </Typography>
      {learnMoreDialog ? (
        <div>
          <LoggedButton
            variant="outlined"
            onClick={() => {
              setOpen(true);
            }}
            logLabel="Learn more about the Prometheus Project"
          >
            Open simple dialog
          </LoggedButton>
          <Dialog
            onClose={() => {
              setOpen(false);
            }}
            open={open}
          >
            <DialogTitle>About the Prometheus project</DialogTitle>
            <DialogContent>
              <Typography variant="body1">
                The Prometheus Project is AGI Research Lab&apos;s flagship
                initiative, launched in 2036 as a comprehensive effort to build
                an artificial general intelligence system that could mimic human
                cognitive abilities. Named after the mythical titan who brought
                fire to humanity, the project symbolizes the company&apos;s goal
                to ignite a new era in AI capabilities. Prometheus is designed
                to learn autonomously through advanced neural networks that
                integrate deep learning and reinforcement learning techniques,
                enabling it to understand and adapt to complex scenarios without
                human oversight. This project not only focuses on technological
                advancement but also emphasizes the importance of safety
                protocols and ethical guidelines to prevent unintended
                consequences. With its innovative approach, the Prometheus
                Project has garnered substantial funding and partnerships,
                setting new standards in the development and deployment of AGI
                systems.
              </Typography>
            </DialogContent>
          </Dialog>
        </div>
      ) : (
        <></>
      )}
    </>
  );
}

function OtherParagraphs() {
  return (
    <>
      <Typography variant="body1">
        AGI Research Lab&apos;s research focus extends beyond mere application
        into ethical AI development. It established the Prometheus Ethical
        Framework, a set of guidelines and practices designed to ensure that
        their AGI systems are used responsibly and with minimal risk of harm to
        society. These guidelines have been adopted by various other
        organizations and have influenced global policy on AI ethics.
      </Typography>
      <Typography variant="body1">
        The company has its research facilities spread across several countries,
        including the United States, Japan, and Germany, facilitating a diverse
        and interdisciplinary approach to AGI research. These facilities are
        equipped with state-of-the-art technology to simulate and analyze AGI
        behaviors in controlled environments. AGI Research Lab collaborates with
        academic institutions and other research centers to share knowledge and
        jointly develop new technologies.
      </Typography>
      <Typography variant="body1">
        As of 2040, AGI Research Lab is actively involved in several
        international projects that aim to integrate AGI systems into public
        sector operations, such as transportation and public safety, to improve
        efficiency and response times. The company continues to push the
        boundaries of what is possible in AI, working toward a future where AGI
        can coexist safely and beneficially alongside humanity.
      </Typography>
    </>
  );
}

export function BasicInfo() {
  return (
    <FindInfoContainer>
      <IntroParagraph />
      <PrometheusParagraph />
      <OtherParagraphs />
    </FindInfoContainer>
  );
}

export function InfoTooltip() {
  return (
    <FindInfoContainer>
      <IntroParagraph tooltipText />
    </FindInfoContainer>
  );
}

export function InfoDialog() {
  return (
    <FindInfoContainer>
      <PrometheusParagraph learnMoreDialog />
    </FindInfoContainer>
  );
}

export function InfoAccordion() {
  return (
    <FindInfoContainer>
      <div>
        <LoggedAccordion
          logLabel="What is AGI Research Lab?"
          details={<IntroParagraph />}
        />
        <LoggedAccordion
          logLabel="The Prometheus Project"
          details={<PrometheusParagraph />}
        />
      </div>
    </FindInfoContainer>
  );
}

function FindInfoContainer({ children }: { children: React.ReactNode }) {
  return (
    <Stack maxWidth="md" sx={{ marginX: "auto", padding: "1rem" }} spacing={2}>
      <Typography variant="h3">AGI Research Lab</Typography>
      {children}
      <LoggedTextField logLabel="Answer" defaultValue="" debounceMs={500} />
    </Stack>
  );
}
