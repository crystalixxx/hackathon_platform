package models

import "time"

type Location struct {
	tableName struct{}  `pg:"location"`
	ID        int       `pg:"id,pk"`
	Title     string    `pg:"title,type:varchar(255),unique"`
	CreatedAt time.Time `pg:"created_at,default:now()"`
	UpdatedAt time.Time `pg:"updated_at"`

	Events []Event `pg:"many2many:event_location"`
}
