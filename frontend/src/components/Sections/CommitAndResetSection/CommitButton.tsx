import { useState } from "react";
import { Button } from "../../../components/ui/button";
import { UserRoundCheck } from "lucide-react";
import { Modal } from "../../../components/core/Modal";
import { pushDataToBackend } from "../../../store/store";

export type CommitButtonProps = {
  disabled?: boolean;
};

export function CommitButton(props: CommitButtonProps) {
  const [showModal, setShowModal] = useState(false);

  const onConfirm = () => {
    pushDataToBackend();
    setShowModal(false);
  };

  const onCancel = () => {
    setShowModal(false);
  };

  return (
    <>
      <Button
        variant="destructive"
        onClick={() => setShowModal(true)}
        disabled={props.disabled}
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
          <div className="flex justify-end gap-2 mt-4">
            <Button
              variant="outline"
              onClick={onCancel}
              className="w-full sm:w-auto"
            >
              No
            </Button>
            <Button
              variant="destructive"
              onClick={onConfirm}
              className="w-full sm:w-auto"
            >
              Yes
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}
