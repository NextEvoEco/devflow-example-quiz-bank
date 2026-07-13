interface EmptyStateProps {
  heading: string
  helper: string
  actionLabel?: string
  onAction?: () => void
}

export function EmptyState({ heading, helper, actionLabel, onAction }: EmptyStateProps) {
  return (
    <div className="empty-state">
      <div className="empty-icon" aria-hidden="true">
        ?
      </div>
      <h2>{heading}</h2>
      <p>{helper}</p>
      {actionLabel && onAction ? (
        <button type="button" className="btn btn-primary" onClick={onAction}>
          {actionLabel}
        </button>
      ) : null}
    </div>
  )
}
