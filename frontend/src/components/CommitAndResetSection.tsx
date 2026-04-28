import { Section } from "./core/Section";
import { CommitButton } from "./inputs/CommitButton";
import { ResetButton } from "./inputs/ResetButton";

export function CommitAndResetSection() {
  return (
    <Section>
      <CommitButton />
      <ResetButton />
    </Section>
  );
}
