import { useState } from "react";
import { Button } from "../ui/button";
import { UserRoundCheck } from "lucide-react";
import { Modal } from "../core/Modal";
import { pushDataToSupabase } from "../../store/store";
import { useAuth } from "../AuthProvider";

export type CommitButtonProps = {
  disabled?: boolean;
};

export function CommitButton(props: CommitButtonProps) {
  const [showModal, setShowModal] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { user, refreshSession } = useAuth();

  const onConfirm = async () => {
    setIsSubmitting(true);
    setSubmitError(null);

    const result = await pushDataToSupabase();

    if (result.success) {
      setShowModal(false);
      setIsSubmitting(false);
      return;
    }

    if (result.error instanceof Error) {
      setSubmitError(result.error.message);
    } else {
      setSubmitError("Failed to commit form.");
    }

    if (
      result.error instanceof Error &&
      result.error.message.toLowerCase().includes("authentication required")
    ) {
      await refreshSession();
    }

    setIsSubmitting(false);
  };

  const onCancel = () => {
    setSubmitError(null);
    setShowModal(false);
  };

  return (
    <>
      <Button
        variant="destructive"
        onClick={() => setShowModal(true)}
        disabled={props.disabled || !user || isSubmitting}
        title={user ? undefined : "Continue with Google before committing data."}
      >
        <UserRoundCheck className="h-5 w-5" />
        Commit Form
      </Button>
      <Modal show={showModal} onDismiss={onCancel}>
        <div className="p-4">
          <h2 className="font-semibold text-3xl text-primary text-center font-rhr-ns tracking-wider">
            Confirm Commit
          </h2>
          <p>Are you sure you want to commit the form?</p>
          {submitError ? (
            <p className="mt-3 rounded border border-red-800 bg-red-950/60 px-3 py-2 text-sm text-red-200">
              {submitError}
            </p>
          ) : null}
          <div className="flex justify-end gap-2 mt-4">
            <Button
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting}
              className="w-full sm:w-auto"
            >
              No
            </Button>
            <Button
              variant="destructive"
              onClick={() => {
                void onConfirm();
              }}
              disabled={isSubmitting}
              className="w-full sm:w-auto"
            >
              {isSubmitting ? "Submitting..." : "Yes"}
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}
