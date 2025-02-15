package models

type EventPrize struct {
	ID           int    `pg:"id,pk"`
	Place        int    `pg:"place"`
	PrimaryPrize string `pg:"description,type:varchar(255)"`
	Description  string `pg:"description"`
	IconURL      string `pg:"icon_url"`

	EventID int
	Event   *Event `pg:"rel:has-one"`
}
