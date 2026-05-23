import { useRef } from 'react';
import { useOnClickOutside } from '../../hooks/useOnClickOutside';
import { CloseButton } from './CloseButton';

export interface ModalProps {
  show: boolean;
  onDismiss?: () => void;
  children?: React.ReactNode;
}

export function Modal(props: ModalProps) {
  const modalRef = useRef(null);
  useOnClickOutside(modalRef, () => props.onDismiss && props.onDismiss());

  return (
    <>
      {props.show && (
        <>
          <div
            className="fixed inset-0 h-full w-full overflow-y-auto bg-zinc-950/70 backdrop-blur"
            id="my-modal"
          />
          <div
            ref={modalRef}
            className="fixed left-1/2 top-20 z-50 w-96 -translate-x-1/2 transform rounded-md bg-card shadow-md"
          >
            <div className="flex flex-row justify-end">
              <CloseButton onClick={props.onDismiss} />
            </div>
            {props.children}
          </div>
        </>
      )}
    </>
  );
}
