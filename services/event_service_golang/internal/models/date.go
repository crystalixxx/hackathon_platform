package models

import "time"

type Date struct {
	tableName struct{}  `pg:"date"`
	ID        int       `pg:"id,pk" example:"1"`
	DateStart time.Time `pg:"date_start" example:"2023-01-01T00:00:00Z"`
	DateEnd   time.Time `pg:"date_end" example:"2023-01-02T00:00:00Z"`

	Events []Event `pg:"rel:has-many"`
	Tracks []Track `pg:"rel:has-many"`
}
