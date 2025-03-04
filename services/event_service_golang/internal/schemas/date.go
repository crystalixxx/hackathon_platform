package schemas

import "time"

type Date struct {
	DateStart time.Time `json:"date_start" validate:"required" example:"2023-01-01T00:00:00Z"`
	DateEnd   time.Time `json:"date_end" validate:"required,gtfield=DateStart" example:"2023-01-02T00:00:00Z"`
}
