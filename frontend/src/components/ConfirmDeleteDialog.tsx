import { useState } from 'react'

interface ConfirmDeleteDialogProps {
  title: string
  message: string
  onCancel: () => void
  onConfirm: () => Promise<void>
}

export function ConfirmDeleteDialog({
  title,
  message,
  onCancel,
  onConfirm,
}: ConfirmDeleteDialogProps) {
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  return (
    <div className="modal-backdrop" onClick={onCancel} role="presentation">
      <div
        className="modal modal-sm"
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-delete-title"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-header">
          <h2 id="confirm-delete-title">{title}</h2>
          <button type="button" className="icon-btn" onClick={onCancel} aria-label="Close">
            ×
          </button>
        </div>
        <div className="modal-body">
          <p>{message}</p>
          {error ? <p className="error-banner">{error}</p> : null}
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-secondary" onClick={onCancel}>
            Cancel
          </button>
          <button
            type="button"
            className="btn btn-danger"
            disabled={busy}
            onClick={async () => {
              setBusy(true)
              setError(null)
              try {
                await onConfirm()
                onCancel()
              } catch (err) {
                setError(err instanceof Error ? err.message : 'Delete failed')
                setBusy(false)
              }
            }}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  )
}
