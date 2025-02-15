package models

type Status struct {
	ID          int    `pg:"id,pk"`
	Title       string `pg:"title,type:varchar(255),unique"`
	Description string `pg:"description"`

	Events []Event `pg:"many2many:status_events"`
	Tracks []Track `pg:"many2many:status_tracks"`
}
