package schemas

type Date struct {
	DateStart string `json:"date_start" validate:"required" example:"2023-01-01T00:00:00Z"`
	DateEnd   string `json:"date_end" validate:"required,gtfield=DateStart" example:"2023-01-02T00:00:00Z"`
}
