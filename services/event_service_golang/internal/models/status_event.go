package models

type StatusEvent struct {
	EventID int    `pg:"event_id,pk"`
	Event   *Event `pg:"rel:has-one"`

	StatusID int     `pg:"status_id,pk"`
	Status   *Status `pg:"rel:has-one"`
}
