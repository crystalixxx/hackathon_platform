package models

type EventLocation struct {
	LocationID int       `pg:"location_id,pk"`
	Location   *Location `pg:"rel:has-one"`

	EventID int    `pg:"event_id,pk"`
	Event   *Event `pg:"rel:has-one"`
}
