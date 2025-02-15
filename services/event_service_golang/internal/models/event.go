package models

import "time"

type Event struct {
	ID           int       `pg:"id,pk"`
	Title        string    `pg:"title,type:varchar(255),unique"`
	Description  string    `pg:"description"`
	RedirectLink string    `pg:"redirect_link"`
	CreatedAt    time.Time `pg:"created_at,default:now()"`
	UpdatedAt    time.Time `pg:"updated_at"`

	DateID int   `pg:"date_id"`
	Date   *Date `pg:"rel:has-one"`

	Locations   []Location   `pg:"many2many:event_locations"`
	Statuses    []Status     `pg:"many2many:status_events"`
	Tracks      []Track      `pg:"rel:has-many"`
	EventPrizes []EventPrize `pg:"rel:has-many"`
}
