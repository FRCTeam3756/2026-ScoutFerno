import { CommitAndResetSection } from "../components/Sections/CommitAndResetSection/CommitAndResetSection";
import { FloatingFormValue } from "../components/FloatingFormValue";
import FormSection from "../components/Sections/FormSection";
import { useScoutFernoState } from "../store/store";

export function Scouting() {
  const formData = useScoutFernoState((state) => state.formData);

  return (
    <main className="flex flex-1 flex-col items-center justify-center px-4 text-center">
      <FloatingFormValue />
      <form className="w-full px-4" onSubmit={(e) => e.preventDefault()}>
        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
          {formData.sections.map((section) => (
            <FormSection key={section.name} name={section.name} />
          ))}
          <CommitAndResetSection />
        </div>
      </form>
    </main>
  );
}