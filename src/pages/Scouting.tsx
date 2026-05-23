import { Section } from "src/components/global/Section";
import FormSection from "../components/scouting/FormSection";
import { useScoutFernoState } from "../store/store";
import { CommitButton } from "src/components/inputs/CommitButton";
import { ResetButton } from "src/components/inputs/ResetButton";

export function Scouting() {
  const formData = useScoutFernoState((state) => state.formData);

  return (
    <main className="flex flex-1 flex-col items-center justify-center px-4 text-center">
      <form className="w-full px-4" onSubmit={(e) => e.preventDefault()}>
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
          {formData.sections.map((section) => (
            <FormSection key={section.name} name={section.name} />
          ))}
          <Section>
            <CommitButton />
            <ResetButton />
          </Section>
        </div>
      </form>
    </main>
  );
}