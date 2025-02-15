package models

import "time"

type Date struct {
	ID        int       `pg:"id,pk"`
	DateStart time.Time `pg:"date_start"`
	DateEnd   time.Time `pg:"date_end"`

	Events []Event `pg:"rel:has-many"`
	Tracks []Track `pg:"rel:has-many"`
}
