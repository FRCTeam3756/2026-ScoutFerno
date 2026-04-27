import { Section } from "../../core/Section";
import { CommitButton } from "./CommitButton";
import { ResetButton } from "./ResetButton";

export function CommitAndResetSection() {
  return (
    <Section>
      <CommitButton />
      <ResetButton />
    </Section>
  );
}
