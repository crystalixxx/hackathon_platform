package models

type Status struct {
	tableName   struct{} `pg:"status"`
	ID          int      `pg:"id,pk"`
	Title       string   `pg:"title,type:varchar(255),unique"`
	Description string   `pg:"description"`

	Events []Event `pg:"many2many:status_event"`
	Tracks []Track `pg:"many2many:status_track"`
}
