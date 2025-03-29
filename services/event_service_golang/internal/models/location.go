package models

type Location struct {
	ID    int    `pg:"id,pk"`
	Title string `pg:"title,type:varchar(255),unique"`

	Events []Event `pg:"many2many:event_location"`
}
