package models

type EventPrize struct {
	ID           int    `pg:"id,pk"`
	Place        int    `pg:"place"`
	PrimaryPrize string `pg:"primary_prize,type:varchar(255),notnull"`
	Description  string `pg:"description"`
	IconURL      string `pg:"icon_url,notnull"`

	EventID int
	Event   *Event `pg:"rel:has-one"`
}
